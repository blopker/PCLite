import unittest
from .. import models
from . import data
import json


class TestRepository(unittest.TestCase):

    def setUp(self):
        self.json = json.loads(data.REPOSITORIES_JSON)
        self.repo = models.Repository(self.json)

    def test_empty_repo(self):
        repo = models.Repository()
        self.assertEqual(0, len(repo.packages))

    def test_merge(self):
        repo = models.Repository()
        repo.merge(self.repo)
        self.assertEqual(len(self.repo.packages), len(repo.packages))

    def test_get_package(self):
        name = 'WordCount'

        p = self.repo.get_package(name)
        self.assertEqual(name, p.name)

        p = self.repo.get_package('not a package')
        self.assertFalse(p)

    def test_install_list(self):
        install_list = self.repo.install_list()

        self.assertIsInstance(install_list, list)
        self.assertEqual(len(install_list), 2)

        packageOne = install_list[0]
        self.assertEqual('WordCount', packageOne[0])
        self.assertEqual('Real time Word Counter.', packageOne[1])
        self.assertIn('2013.03', packageOne[2])

        packageTwo = install_list[1]
        self.assertEqual('23', packageTwo[1])
