
import pkg_resources
from importlib import import_module

from generallibrary import ObjInfo


class LocalModule:
    """ Tools to interface a Local Python Module. """
    def __init__(self, name):
        self.name = name

        self.module = import_module(name=self.name)

        self.objInfo = ObjInfo(self.module)
        assert self.objInfo.is_module()
        self.objInfo.filters = [self._filter]
        self.objInfo.get_attrs(depth=-1)

    @classmethod
    def is_creatable(cls, name):
        """ Return whether this API can be created. """
        try:
            import_module(name=name)
        except ModuleNotFoundError:
            return False
        return True

    def _filter(self, objInfo):
        """ :param ObjInfo objInfo: """
        is_part_of_module = getattr(objInfo.module(), "__name__", "").startswith(self.module.__name__)
        return objInfo.public() and (objInfo.is_class() or objInfo.is_method()) and is_part_of_module

    def get_env_vars(self):
        """ Get a list of EnvVar instances avialable directly in module.

            :rtype: list[generallibrary.EnvVar] """
        objInfo = ObjInfo(self.module)
        objInfo.filters = [lambda objInfo: type(objInfo.obj).__name__ == "EnvVar"]
        objInfo.get_attrs()
        return [objInfo.obj for objInfo in objInfo.get_children()]

    @staticmethod
    def get_all_packages():
        """ Get a list of all available packages. """
        return [pkg.project_name for pkg in pkg_resources.working_set]

    def get_dependencies(self, name=None):
        """ Get a list of dependencies' names this module has. """
        if name is None:
            name = self.module.__name__
        return list(map(str, pkg_resources.working_set.by_key[name.lower()].requires()))

    def get_dependants(self, name=None):
        """ Get a list of all available packages' names. """
        if name is None:
            name = self.module.__name__
        return [pkg for pkg in self.get_all_packages() if name.lower() in self.get_dependencies(name=pkg)]


























