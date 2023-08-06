
from generallibrary import Ver, deco_cache
from generalfile import Path

import requests
import re
import shutil


def download(url, path):
    """ Todo: Move download to it's own package.
        Todo: Binary extension for generalfile. """
    data = requests.get(url)
    path = Path(path)

    with path.lock():
        path.get_parent().create_folder()
        with open(str(path), "wb") as file:
            file.write(data.content)


def unpack(path, target):
    """ Todo: Add pack and unpack to generalfile. """
    shutil.unpack_archive(str(path), str(target))


class PyPI:
    """ Tools to interface pypi.org """
    def __init__(self, name):
        self.name = name

        self.url = self.get_url(name=self.name)

    @classmethod
    def is_creatable(cls, name):
        """ Return whether this API can be created. """
        return requests.get(url=cls.get_url(name=name)).status_code == 200

    @staticmethod
    def get_url(name):
        """ Get static URL from owner and name. """
        return f"https://pypi.org/project/{name}/"

    @deco_cache()
    def get_tarball_url(self, name=None, version=None):
        """ Get URL to download tarball. """
        if name is None:
            name = self.name
        if version is None:
            version = self.get_version(name=name)
        return f"https://pypi.io/packages/source/{name[0]}/{name}/{name}-{version}.tar.gz"

    def download_and_unpack_tarball(self, target_folder, name=None, version=None):
        """ Download tar ball, extract it, remove tar ball. """
        temp = Path.get_cache_dir() / "Python/temp.tar.gz"
        download(self.get_tarball_url(name=name, version=version), path=temp)
        unpack(path=temp, target=target_folder)
        temp.delete(error=False)
        return target_folder

    @staticmethod
    @deco_cache()
    def get_users_packages(user=None):
        """ Get a set of a user's packages' names on PyPI. """
        if user is None:
            user = "Mandera"
        return set(re.findall("/project/(.*)/", requests.get(f"https://pypi.org/user/{user}/").text))

    @deco_cache()
    def get_version(self, name=None):
        """ Get version of latest publish on PyPI. """
        if name is None:
            name = self.name
        return Ver(re.findall(f"{name} ([.0-9]+)\n", requests.get(f"https://pypi.org/project/{name}/").text)[0])

    # @deco_cache()
    def get_datetime(self, name=None):
        """ Get datetime of latest release.
            Todo: Proper date fetch. """
        if name is None:
            name = self.name
        requests.get(f"https://pypi.org/project/{name}/")
        result = re.findall('Generated (.+) for commit', requests.get(f"https://pypi.org/project/{name}/").text)
        return result[0] if result else "-"

    def reserve_name(self):
        pass


























