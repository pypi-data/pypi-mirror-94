
from generallibrary import CodeLine, comma_and_and, EnvVar


class _PackagerWorkflow:
    """ Light handling of workflow logic. """
    @staticmethod
    def _var(string):
        return f"${{{{ {string} }}}}"

    @staticmethod
    def _commit_msg_if(**conditions):
        checks = [f"contains(github.event.head_commit.message, '[CI {key}]') == {str(value).lower()}" for key, value in conditions.items()]
        return f"if: {' && '.join(checks)}"

    _commit_msg = "github.event.head_commit.message"
    _action_checkout = "actions/checkout@v2"
    _action_setup_python = "actions/setup-python@v2"
    _matrix_os = "matrix.os"
    _matrix_python_version = "matrix.python-version"

    def get_triggers(self):
        """ :param generalpackager.Packager self: """
        on = CodeLine("on:")
        push = on.add("push:")
        branches = push.add("branches:")
        branches.add("- master")
        return on

    def get_step(self, name, *codelines):
        """ . """
        step = CodeLine(f"- name: {name}")
        for codeline in codelines:
            if codeline:
                step.add(codeline)
        return step

    def step_setup_python(self, version):
        """ :param generalpackager.Packager self:
            :param version: """
        with_ = CodeLine("with:")
        with_.add(f"python-version: {version}")
        return self.get_step(f"Set up python version {version}", f"uses: {self._action_setup_python}", with_)

    def step_install_necessities(self):
        """ :param generalpackager.Packager self: """
        run = CodeLine("run: |")
        run.add("python -m pip install --upgrade pip")
        run.add(f"pip install setuptools wheel twine")
        return self.get_step(f"Install necessities pip, setuptools, wheel, twine", run)

    def step_install_package_pip(self, *packages):
        """ Supply package name as it's stated on pypi.

            :param generalpackager.Packager self: """
        run = CodeLine(f"run: pip install {' '.join(packages)}")
        return self.get_step(f"Install pip packages {comma_and_and(*packages, period=False)}", run)

    def step_install_package_git(self, *author_repo_tuple):
        """ Supply author/repo, e.g. ManderaGeneral/generalpackager

            :param generalpackager.Packager self: """
        assert all(map(lambda x: "/" in x, author_repo_tuple))

        run = CodeLine(f"run: |")
        for author_repo in author_repo_tuple:
            run.add(f"pip install git+https://github.com/{author_repo}.git")

        return self.get_step(f"Install {len(author_repo_tuple)} git repos", run)

    def get_env(self):
        """ :param generalpackager.Packager self: """
        env = CodeLine("env:")
        for packager in self.get_nodes_all():
            for env_var in packager.localmodule.get_env_vars():
                if env_var.actions_name and env_var.name not in str(env):
                    env.add(f"{env_var.name}: {env_var.actions_name}")
        if not env.get_children():
            return None
        return env

    def steps_setup(self, python_version):
        """ :param generalpackager.Packager self:
            :param python_version: """
        steps = CodeLine("steps:")
        steps.add(self.step_setup_python(version=python_version))
        steps.add(self.step_install_necessities())
        steps.add(self.step_install_package_git(
            *[f"{packager.github.owner}/{packager.name}" for packager in self.get_ordered_packagers()]))
        return steps

    def get_unittest_job(self):
        """ :param generalpackager.Packager self: """
        job = CodeLine("unittest:")
        job.add(self._commit_msg_if(SKIP=False, AUTO=False))
        job.add(f"runs-on: {self._var(self._matrix_os)}")
        strategy = job.add("strategy:")
        matrix = strategy.add("matrix:")
        matrix.add(f"python-version: {list(self.python)}".replace("'", ""))
        matrix.add(f"os: {[f'{os}-latest' for os in self.os]}".replace("'", ""))

        steps = job.add(self.steps_setup(python_version=self._var(self._matrix_python_version)))
        steps.add(self.step_run_packager_method("workflow_unittest"))
        return job

    def get_sync_job(self):
        """ :param generalpackager.Packager self: """
        job = CodeLine("sync:")
        job.add("needs: unittest")
        job.add(f"runs-on: ubuntu-latest")
        steps = job.add(self.steps_setup(python_version=self.python[0]))
        steps.add(self.step_run_packager_method("workflow_sync"))
        return job

    def step_run_packager_method(self, method):
        """ :param generalpackager.Packager self:
            :param method: """
        run = CodeLine(f'run: |')
        run.add(f'python -c "from generalpackager import Packager; Packager(\'generalpackager\', \'\').{method}()"')
        return self.get_step(f"Run Packager method '{method}'", run, self.get_env())

    def run_ordered_methods(self, *funcs):
        """ :param generalpackager.Packager self: """
        self.load_general_packagers()
        order = self.get_ordered_packagers()
        for func in funcs:
            for packager in order:
                func(packager=packager)

    def workflow_unittest(self):
        """ :param generalpackager.Packager self: """
        self.run_ordered_methods(
            lambda packager: packager.generate_localfiles(aesthetic=False),
            lambda packager: packager.localrepo.pip_install(),
            lambda packager: packager.localrepo.unittest(),
        )

    def workflow_sync(self):
        """ Runs in workflow once Packagers have created each LocalRepo from latest master commit.

            :param generalpackager.Packager self: """
        trigger_repo = str(EnvVar('GITHUB_REPOSITORY')).split('/')[1]
        msg1 = f"[CI AUTO] Sync triggered by {trigger_repo}"
        msg2 = f"[CI AUTO] Publish triggered by {trigger_repo}"

        self.run_ordered_methods(
            lambda packager: packager.if_publish_bump(),
            lambda packager: packager.generate_localfiles(aesthetic=True),
            lambda packager: packager.localrepo.pip_install(),
            lambda packager: packager.localrepo.unittest(),  # For good measure
            lambda packager, msg=msg1: packager.commit_push_store_sha(message=msg, tag=False),
            lambda packager, msg=msg2: packager.if_publish_publish(message=msg),
            lambda packager: packager.sync_github_metadata(),
        )

        mandera = type(self)(name="Mandera", owner="Mandera")
        mandera.file_personal_readme.generate()
        mandera.commit_push_store_sha(message=msg1)

    def if_publish_bump(self):
        """ :param generalpackager.Packager self: """
        if self.general_bumped_set() and not self.is_bumped() and self.compare_local_to_pypi(aesthetic=False):
            self.localrepo.bump_version()

    def if_publish_publish(self, message):
        """ :param generalpackager.Packager self:
            :param message: """
        if self.is_bumped():
            self.file_readme.generate()
            self.commit_push_store_sha(message=message, tag=True)
            self.localrepo.upload()







