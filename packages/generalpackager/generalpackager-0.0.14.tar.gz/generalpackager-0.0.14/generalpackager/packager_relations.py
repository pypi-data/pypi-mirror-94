

class _PackagerRelations:
    packagers_dict = {}

    def add(self):
        """ Add this packager to packagers dict.

            :param generalpackager.Packager self: """
        if self.name in self.packagers_dict:
            raise AttributeError(f"{self.name} packager already exists")

        self.packagers_dict[self.name] = self

    def remove(self):
        """ Remove this packager from packagers dict.

            :param generalpackager.Packager self: """
        self.packagers_dict.pop(self.name)

    def update_links(self):
        """ Update links of all created Packagers.

            :param generalpackager.Packager self: """
        for packager in self.packagers_dict.values():
            for dependency_name in packager.localrepo.install_requires:
                dependency_packager = self.packagers_dict.get(dependency_name)
                if dependency_packager is not None:
                    dependency_packager.link(target=packager)

    def get_packager_with_name(self, name):
        """ Return connected Packager or None.

            :param generalpackager.Packager self:
            :param name: """
        if self.name == name:
            return self

        packager = self.packagers_dict.get(name)
        if packager is None and self.is_creatable(name=name):
            packager = type(self)(name=name, repos_path=self.repos_path)

        return packager

    def load_general_packagers(self):
        """ Load packagers with names.

            :param generalpackager.Packager self: """
        if not self.packagers_dict:
            for name in self.get_users_package_names():
                packager = self.get_packager_with_name(name=name)

                if packager and packager.localrepo.enabled:
                    packager.add()
                    self.update_links()
        return self.packagers_dict

    def get_dependencies(self):
        """ Get set of loaded Packagers that this Packager requires.

            :param generalpackager.Packager self: """
        return self.get_nodes(incoming=True, outgoing=False)

    def get_dependents(self):
        """ Get set of loaded Packagers that requires this Packager.

            :param generalpackager.Packager self: """
        return self.get_nodes(incoming=False, outgoing=True)

    def get_ordered_packagers(self):
        """ Get a list of ordered names from the dependency chain.

            :param generalpackager.Packager self: """
        return [packager for packager_set in self.get_ordered() for packager in sorted(packager_set, key=lambda x: x.name)]

    @classmethod
    def get_users_package_names(cls, pypi_user=None, github_user=None):
        """ Return a set of user's packages with intersecting PyPI and GitHub.

            :param generalpackager.Packager cls:
            :param pypi_user:
            :param github_user: """
        return cls.PyPI.get_users_packages(user=pypi_user).intersection(cls.GitHub.get_users_packages(user=github_user))

    def general_bumped_set(self):
        """ Return a set of general packagers that have been bumped.

            :param generalpackager.Packager self: """
        self.load_general_packagers()
        return {packager for packager in self.packagers_dict.values() if packager.is_bumped()}

    def general_changed_dict(self, aesthetic=False):
        """ Return a dict of general packagers with changed files comparing to remote.

            :param generalpackager.Packager self:
            :param aesthetic: """
        self.load_general_packagers()
        return {packager: files for packager in self.packagers_dict.values() if (files := packager.compare_local_to_remote(aesthetic=aesthetic))}

