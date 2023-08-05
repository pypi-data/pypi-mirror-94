
import unittest
import random

from generalpackager import GitHub


# Running tests locally:            Set env var 'packager_github_api' to GitHub token, run unittests with PyCharm as usual
# Running tests in GitHub Actions:  Run test.main and supply env vars as launch options.

class TestGitHub(unittest.TestCase):
    def test_topics(self):
        github = GitHub("generalpackager")
        self.assertTrue(github.get_topics())
