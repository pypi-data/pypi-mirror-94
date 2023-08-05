
from generallibrary import NetworkDiagram

from generalpackager import Packager
from generalpackager.api.local_repo import LocalRepo


# class PackagerNetwork(NetworkDiagram):
#     def __init__(self, packager):
#         self.packager = packager


# class PackagerGrp(list):
#     """ Handles a collection of packages.
#         Todo: Maybe move PackagerGrp to Packager now that it inherits NetworkDiagram? """
#     def __init__(self, *packagers, repos_path=None):
#         super().__init__(packagers)
#
#         self.repos_path = LocalRepo.get_repos_path(path=repos_path)
#
#         self.load_general_packages()
#
#     def load_general_packages(self):
#         """ Load my general packages. """
#         self.add_packages_from_names(*Packager.get_users_package_names())
#
#     def add_packages_from_names(self, *names):
#         """ Add a Package. """
#         self.extend([Packager(name=name, repos_path=self.repos_path) for name in names])
#
#     def clone(self):
#         """ Clone all packages to repos_path. """
#         for packager in self:
#             packager.clone_repo()
#
#     def install(self):
#         """ Install all packages. """
#         for packager in self:
#             packager.localrepo.pip_install()
#
#     def get_bumped(self):
#         """ Get a list of bumped packagers, meaning PyPI version and LocalRepo version mismatch. """
#         # return [(packager.localrepo.version, packager.pypi.get_version()) for packager in self.packagers if packager.is_bumped()]
#         return [packager for packager in self if packager.is_bumped()]



