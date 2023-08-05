
from generalfile import Path
from generalpackager import GIT_PASSWORD
from generallibrary import Ver, deco_cache

from setuptools import find_namespace_packages
import re
from git import Repo
import subprocess
import sys


class LocalRepo:
    """ Tools to help Path interface a Local Python Repository. """
    enabled = True
    name = ...
    version = "0.0.1"  # type: Ver
    description = "Missing description."
    install_requires = []
    extras_require = {}
    topics = []
    manifest = []

    metadata_keys = [key for key, value in locals().items() if not key.startswith("_")]

    def __init__(self, path, git_exclude_lines):
        assert self.path_is_repo(path=path)

        self.path = Path(path).absolute()
        self.git_exclude_lines = git_exclude_lines

        self.has_metadata = self.get_metadata_path().exists(quick=True)
        if self.has_metadata:
            for key, value in self.get_metadata_path().read().items():
                setattr(self, f"_{key}", value)

        if self.extras_require:
            self.extras_require["full"] = list(set().union(*self.extras_require.values()))
            self.extras_require["full"].sort()

        self.version = Ver(self.version)

        if self.name is Ellipsis:
            self.name = self.path.name()

    @staticmethod
    def get_repos_path(path):
        """ Try to return repos path by iterating parents if None. """
        if path is None:
            repos_path = Path.get_working_dir()
            while not LocalRepo.get_local_repos(repos_path):
                repos_path = repos_path.get_parent()
                if repos_path is None:
                    raise AttributeError(f"Couldn't find repos path.")
            return repos_path
        else:
            return Path(path).absolute()

    @classmethod
    def is_creatable(cls, path):
        """ Return whether this API can be created. """
        return cls.path_is_repo(path=path)

    def metadata_setter(self, key, value):
        """ Set a metadata's key both in instance and json file. """
        if self.has_metadata and value != getattr(self, f"_{key}", ...):
            metadata = self.get_metadata_path().read()
            metadata[key] = str(value)
            self.get_metadata_path().write(metadata, overwrite=True, indent=4)

        setattr(self, f"_{key}", value)

    def get_readme_path(self):
        """ Get a Path instance pointing to README.md, regardless if it exists. """
        return self.path / "README.md"

    def get_metadata_path(self):
        """ Get a Path instance pointing to metadata.json, regardless if it exists. """
        return self.path / "metadata.json"

    def get_git_exclude_path(self):
        """ Get a Path instance pointing to .git/info/exclude, regardless if it exists. """
        return self.path / ".git/info/exclude"

    def get_setup_path(self):
        """ Get a Path instance pointing to setup.py, regardless if it exists. """
        return self.path / "setup.py"

    def get_manifest_path(self):
        """ Get a Path instance pointing to MANIFEST.in, regardless if it exists. """
        return self.path / "MANIFEST.in"

    def get_license_path(self):
        """ Get a Path instance pointing to LICENSE, regardless if it exists. """
        return self.path / "LICENSE"

    def get_workflow_path(self):
        """ Get a Path instance pointing to workflow.yml, regardless if it exists. """
        return self.path / ".github/workflows/workflow.yml"

    def get_test_path(self):
        """ Get a Path instance pointing to workflow.yml, regardless if it exists. """
        return self.path / f"{self.name}/test"

    def get_package_paths(self):
        """ Get a list of Paths pointing to each folder containing a Python file in this local repo, aka `namespace package`. """
        return [self.path / pkg.replace(".", "/") for pkg in find_namespace_packages(where=str(self.path))]

    @classmethod
    def get_local_repos(cls, folder_path):
        """ Return a list of local repos in given folder. """
        folder_path = Path(folder_path)
        if not folder_path.exists():
            return []
        return [path for path in folder_path.get_paths_in_folder() if cls.path_is_repo(path)]

    @classmethod
    def path_is_repo(cls, path):
        """ Return whether this path is a local repo. """
        path = Path(path)
        if path.is_file() or not path.exists(quick=True):
            return False
        return ".git" in map(Path.name, path.get_paths_in_folder())

    @deco_cache()
    def get_todos(self):
        """ Get a list of dicts containing cleaned up todos.

            :rtype: dict[list[str]] """
        todos = []
        for path in self.path.get_paths_recursive():
            if path.match(*self.git_exclude_lines, "shelved.patch", "readme.md"):
                continue
            try:
                text = path.text.read()
            except:
                continue

            for todo in re.findall("todo+: (.+)", text, re.I):
                todos.append({
                    "Module": path.name(),
                    "Message": re.sub('[" ]*$', "", todo),
                })
        return todos

    def commit_and_push(self, message=None, tag=False, owner=None):
        """ Commit and push this local repo to GitHub.
            Return short sha1 of pushed commit. """
        if message is None:
            message = "Automatic commit."
        if owner is None:
            owner = "ManderaGeneral"

        repo = Repo(str(self.path))

        repo.git.add(A=True)
        repo.index.commit(message=str(message))
        remote = repo.remote()
        remote.set_url(f"https://Mandera:{GIT_PASSWORD}@github.com/{owner}/{self.name}.git")

        if tag:
            tag_ref = repo.create_tag(f"v{self.version}", force=True)
            remote.push(refspec=tag_ref)

        return remote.push()[0].summary.split("..")[1].rstrip()

    def get_changed_files(self):
        """ Get a list of changed files compared to remote. """
        repo = Repo(str(self.path))
        return re.findall("diff --git a/(.*) " + "b/", repo.git.diff())

    def bump_version(self):
        """ Bump micro version in metadata.json. """
        self.version = self.version.bump()

    def pip_install(self):
        """ Install this repository with pip, WITHOUT -e flag.
            Subprocess messed up -e flag compared to doing it in terminal, so use the normal one."""
        subprocess.check_call([sys.executable, "-m", "pip", "install", str(self.path)])

    def unittest(self):
        """ Run unittests for this repository. """
        subprocess.check_call([sys.executable, "-m", "unittest", "discover", str(self.get_test_path())])

    def create_sdist(self):
        """ Create source distribution. """
        with self.path.as_working_dir():
            subprocess.check_call([sys.executable, "setup.py", "sdist", "bdist_wheel"])

    def upload(self):
        """ Upload local repo to PyPI. """
        self.create_sdist()
        with self.path.as_working_dir():
            subprocess.check_call([sys.executable, "-m", "twine", "upload", "dist/*"])

for key in LocalRepo.metadata_keys:
    value = getattr(LocalRepo, key)
    setattr(LocalRepo, key, property(
        fget=lambda self, key=key, value=value: getattr(self, f"_{key}", value),
        fset=lambda self, value, key=key: LocalRepo.metadata_setter(self, key, value),
    ))


































