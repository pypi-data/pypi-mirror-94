
from generallibrary import CodeLine, current_datetime, Markdown
from generalfile import Path


class GenerateFile:
    """ Handle generation of files. """
    def __init__(self, path, text_func, packager, aesthetic):
        self.text_func = text_func
        self.packager = packager
        self.aesthetic = aesthetic

        self.relative_path = path.relative(base=packager.path)
        self.path = packager.path / self.relative_path

    def generate(self):
        """ Generate actual file. """
        self.path.text.write(f"{self.text_func()}\n", overwrite=True)


class _PackagerFiles:
    """ Generates setup, license and gitexclude.
        Only changed non-aesthetic files can trigger a version bump and publish. """
    extra_aesthetic = "randomtesting.py",  # "licenses"
    extra_non_aesthetic = tuple()

    def __init_post__(self):
        """ Todo: Watermark generated files to prevent mistake of thinking you can modify them directly.

            :param generalpackager.Packager self: """
        self.file_setup =           GenerateFile(self.localrepo.get_setup_path(), self.generate_setup, self, aesthetic=False)
        self.file_manifest =        GenerateFile(self.localrepo.get_manifest_path(), self.generate_manifest, self, aesthetic=False)

        self.file_git_exclude =     GenerateFile(self.localrepo.get_git_exclude_path(), self.generate_git_exclude, self, aesthetic=True)
        self.file_license =         GenerateFile(self.localrepo.get_license_path(), self.generate_license, self, aesthetic=True)
        self.file_workflow =        GenerateFile(self.localrepo.get_workflow_path(), self.generate_workflow, self, aesthetic=True)
        self.file_readme =          GenerateFile(self.localrepo.get_readme_path(), self.generate_readme, self, aesthetic=True)

        self.files = [getattr(self, key) for key in dir(self) if key.startswith("file_")]
        self.files_by_relative_path = {file.relative_path: file for file in self.files}

        self.file_personal_readme = GenerateFile(self.localrepo.get_readme_path(), self.generate_personal_readme, self, aesthetic=True)

    def relative_path_is_aesthetic(self, relative_path):
        """ Relative to package path. None if not defined as a GenerateFile instance.

            :param generalpackager.Packager self:
            :param Path relative_path: """
        aesthetic_attr = getattr(self.files_by_relative_path.get(relative_path, None), "aesthetic", None)
        if aesthetic_attr is None:
            if relative_path.match(*self.extra_aesthetic):
                return True
            elif relative_path.match(*self.extra_non_aesthetic):
                return False
        return aesthetic_attr

    def filter_relative_filenames(self, *filenames, aesthetic, non_defined=True):
        """ If aesthetic is None then it doesn't filter any.
            True will return only aesthetic.
            False will return only non-aesthetic.

            :param generalpackager.Packager self:
            :param bool or None aesthetic:
            :param bool non_defined: """
        result = []
        for filename in filenames:
            is_aesthetic = self.relative_path_is_aesthetic(filename)
            if non_defined is False and is_aesthetic is None:
                continue
            if aesthetic is True and is_aesthetic is False:
                continue
            if aesthetic is False and is_aesthetic is True:
                continue
            result.append(filename)
        return result

    def compare_local_to_remote(self, aesthetic=None):
        """ Get a list of changed files compared to remote with optional aesthetic files.

            :param generalpackager.Packager self:
            :param aesthetic: """
        return self.filter_relative_filenames(*self.localrepo.get_changed_files(), aesthetic=aesthetic)

    def generate_setup(self):
        """ Generate setup.py.

            :param generalpackager.Packager self: """
        readme_path = self.localrepo.get_readme_path().relative(self.localrepo.get_setup_path().get_parent())
        last_version_split = self.python[-1].split(".")
        last_version_bumped_micro = f"{last_version_split[0]}.{int(last_version_split[1]) + 1}"
        setup_kwargs = {
            "name": f'"{self.localrepo.name}"',
            "author": f"'{self.author}'",
            "author_email": f'"{self.email}"',
            "version": f'"{self.localrepo.version}"',
            "description": f'"{self.localrepo.description}"',
            "long_description": f"(Path(__file__).parent / '{readme_path}').read_text(encoding='utf-8')",
            "long_description_content_type": '"text/markdown"',
            "install_requires": self.localrepo.install_requires,
            "url": f'"{self.github.url}"',
            "license": f'"{self.license}"',
            "python_requires": f'">={self.python[0]}, <{last_version_bumped_micro}"',
            "packages": 'find_namespace_packages(exclude=("build*", "dist*"))',
            "extras_require": self.localrepo.extras_require,
            "classifiers": self.get_classifiers(),
            # "include_package_data": True,
        }

        top = CodeLine()
        top.add(CodeLine("from setuptools import setup, find_namespace_packages", space_before=1))
        top.add(CodeLine("from pathlib import Path", space_after=1))

        setup = top.add(CodeLine("setup("))
        for key, value in setup_kwargs.items():
            if isinstance(value, list) and value:
                list_ = setup.add(CodeLine(f"{key}=["))
                for item in value:
                    list_.add(CodeLine(f"'{item}',"))
                setup.add(CodeLine("],"))
            elif isinstance(value, dict) and value:
                dict_ = setup.add(CodeLine(f"{key}={{"))
                for k, v in value.items():
                    dict_.add(CodeLine(f"'{k}': {v},"))
                setup.add(CodeLine("},"))
            else:
                setup.add(CodeLine(f"{key}={value},"))

        top.add(CodeLine(")"))

        return top.text()

    def generate_manifest(self):
        """ Generate manifest file.

            :param generalpackager.Packager self: """
        default_manifest = [
            self.localrepo.get_metadata_path().relative(self.path),
        ]
        return "\n".join([f"include {path}" for path in self.localrepo.manifest + default_manifest])

    def generate_git_exclude(self):
        """ Generate git exclude file.

            :param generalpackager.Packager self: """
        return "\n".join(self.git_exclude_lines)

    def generate_license(self):
        """ Generate LICENSE by using Packager.license.

            :param generalpackager.Packager self: """
        text = Path(self.repos_path / f"generalpackager/generalpackager/licenses/{self.license}").text.read()
        assert "$" in text
        text = text.replace("$year", str(current_datetime().year))
        text = text.replace("$author", self.author)
        assert "$" not in text

        return text

    def generate_workflow(self):
        """ Generate workflow.yml.

            :param generalpackager.Packager self: """
        workflow = CodeLine()
        workflow.indent_str = " " * 2

        workflow.add("name: workflow")
        workflow.add(self.get_triggers())

        jobs = workflow.add("jobs:")
        jobs.add(self.get_unittest_job())
        jobs.add(self.get_sync_job())

        return workflow.text()

    def generate_readme(self):
        """ Generate readme markdown and overwrite README.md in local repo.

            :param generalpackager.Packager self: """
        # Description
        markdown = self.get_description_markdown()

        # Information
        self.get_information_markdown().set_parent(parent=markdown)

        # Table of contents
        contents = Markdown(header="Contents", parent=markdown)

        # Installation
        self.get_installation_markdown().set_parent(parent=markdown)

        # Attributes
        self.get_attributes_markdown().set_parent(parent=markdown)

        # Todos
        todos = self.localrepo.get_todos()
        if todos:
            Markdown(header=f"Todo ({len(todos)}x)", parent=markdown).add_table_lines(*todos)

        # Table of contents - Configuration
        self.configure_contents_markdown(markdown=contents)

        # Footnote
        self.get_footnote_markdown().set_parent(parent=markdown)

        return markdown

    def generate_personal_readme(self):
        """ Generate personal readme markdown and overwrite README.md in local repo.

            :param generalpackager.Packager self: """
        # Description
        markdown = Markdown(header="General").add_list_lines(
            "A collection of connected packages.",
            "Violently updated with little regard for backwards compatability.",
            "Automatic workflows to unittest, sync and publish.",
        )

        # Package information
        self.get_information_markdown(*self.load_general_packagers().values()).set_parent(parent=markdown)

        # Footnote
        self.get_footnote_markdown(commit=False).set_parent(parent=markdown)

        return markdown




























