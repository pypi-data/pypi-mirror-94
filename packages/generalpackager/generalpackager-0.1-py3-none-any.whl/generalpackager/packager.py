""" Methods specific for my general packages.
    Isolatable methods are put inside APIs. """

from generallibrary import initBases, NetworkDiagram
from generalpackager import LocalRepo, LocalModule, GitHub, PyPI

from generalpackager.packager_files import _PackagerFiles
from generalpackager.packager_github import _PackagerGitHub
from generalpackager.packager_markdown import _PackagerMarkdown
from generalpackager.packager_metadata import _PackagerMetadata
from generalpackager.packager_pypi import _PackagerPypi
from generalpackager.packager_workflow import _PackagerWorkflow
from generalpackager.packager_relations import _PackagerRelations


@initBases
class Packager(NetworkDiagram, _PackagerMarkdown, _PackagerGitHub, _PackagerFiles, _PackagerMetadata, _PackagerPypi, _PackagerWorkflow, _PackagerRelations):
    """ Uses APIs to manage 'general' package.
        Contains methods that require more than one API as well as methods specific for ManderaGeneral.
        Todo: Allow github, pypi or local repo not to exist in any combination.
        Todo: Replace badges with generated hardcode.
        Todo: Find all imports to generate install_requires.
        Todo: Create links for Todos. """

    LocalRepo, LocalModule, GitHub, PyPI = LocalRepo, LocalModule, GitHub, PyPI

    author = 'Rickard "Mandera" Abraham'
    email = "rickard.abraham@gmail.com"
    license = "mit"
    python = "3.8", "3.9"  # Only supports basic definition with tuple of major.minor.
    os = "windows", "ubuntu"  # , "macos"

    git_exclude_lines = ".idea", "build", "dist", "*.egg-info", "__pycache__", ".git"

    def __init__(self, name, repos_path=None, owner=None):
        if owner is None:
            owner = "ManderaGeneral"

        self.name = name
        self.repos_path = LocalRepo.get_repos_path(path=repos_path)
        self.owner = owner

        self.path = self.repos_path / self.name

        self._localrepo = None
        self._github = None
        self._localmodule = None
        self._pypi = None

    def is_creatable(self, name):
        """ Simple placeholder check. """
        # return LocalRepo.is_creatable(path=self.repos_path / name)
        return GitHub.is_creatable(name=name, owner="ManderaGeneral")

    @property
    def localrepo(self):
        """ Generate, protect and cache. """
        if not self._localrepo:
            if not LocalRepo.is_creatable(path=self.path):
                if self.github:
                    self.clone_repo(url=self.github.url, path=self.path)
                else:
                    return None
            self._localrepo = LocalRepo(path=self.path, git_exclude_lines=self.git_exclude_lines)

        return self._localrepo

    @property
    def github(self):
        """ Generate, protect and cache. """
        if not self._github:
            self._github = GitHub(name=self.name, owner=self.owner)

        return self._github

    @property
    def localmodule(self):
        """ Generate, protect and cache. """
        if not self._localmodule:
            self._localmodule = LocalModule(name=self.name)

        return self._localmodule

    @property
    def pypi(self):
        """ Generate, protect and cache. """
        if not self._pypi:
            self._pypi = PyPI(name=self.name)
        return self._pypi

    def generate_localfiles(self, aesthetic=True):
        """ Generate all local files. """
        for generate in self.files:
            if aesthetic or not generate.aesthetic:
                generate.generate()

    def __repr__(self):
        return f"<Packager: {self.name}>"


















































