
from generalpackager import PACKAGER_GITHUB_API

import requests
import json
import re


class GitHub:
    """ Tools to interface a GitHub Repository. """
    def __init__(self, name, owner=None):
        if owner is None:
            owner = "ManderaGeneral"

        self.name = name
        self.owner = owner

        self.url = self.get_url(name=self.name, owner=self.owner)

        # if not self.is_url_functioning():
        #     raise AssertionError(f"Url for {self.name} is not functioning.")

    @classmethod
    def is_creatable(cls, name, owner):
        """ Return whether this API can be created. """
        return requests.get(url=cls.get_url(name=name, owner=owner)).status_code == 200

    @staticmethod
    def get_url(name, owner):
        """ Get static URL from owner and name. """
        return f"https://github.com/{owner}/{name}"

    def is_url_functioning(self, url=None):
        """ Checks name, owner and token all in one. """
        return self._request(url=url).status_code == 200

    def api_url(self, endpoint=None):
        """ Get URL from owner, name and enpoint. """
        return "/".join(("https://api.github.com", "repos", self.owner, self.name) + ((endpoint, ) if endpoint else ()))

    def get_website(self):
        """ Get website specified in repository details.

            :rtype: list[str] """
        return self._request(method="get").json()["homepage"]

    def set_website(self, website):
        """ Set a website for the GitHub repository. """
        return self._request(method="patch", name=self.name, homepage=website)


    def get_topics(self):
        """ Get a list of topics in the GitHub repository.

            :rtype: list[str] """
        return self._request(method="get", endpoint="topics").json()["names"]

    def set_topics(self, *topics):
        """ Set topics for the GitHub repository.

            :param str topics: """
        return self._request(method="put", endpoint="topics", names=topics)


    def get_description(self):
        """ Get a string of description in the GitHub repository.

            :rtype: list[str] """
        return self._request(method="get").json()["description"]

    def set_description(self, description):
        """ Set a description for the GitHub repository. """
        return self._request(method="patch", name=self.name, description=description)

    def _request(self, method="get", url=None, endpoint=None, **data):
        """ :rtype: requests.Response """
        method = getattr(requests, method.lower())

        kwargs = {
            "headers": {"Accept": "application/vnd.github.mercy-preview+json"},
            "auth": (self.owner, PACKAGER_GITHUB_API.value),
        }
        if data:
            kwargs["data"] = json.dumps(data)

        if url is None:
            url = self.api_url(endpoint=endpoint)
        return method(url=url, **kwargs)

    @staticmethod
    def get_users_packages(user=None):
        """ Get a set of a user's packages' names on GitHub. """
        if user is None:
            user = "ManderaGeneral"
        return set(re.findall(f'"/{user}/([a-z]*)"', requests.get(f"https://github.com/{user}?tab=repositories").text))















