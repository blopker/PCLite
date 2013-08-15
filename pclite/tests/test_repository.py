import unittest
import sublime
from .. import repository
import json

test_channel = sublime.load_resource('Packages/PCLite/pclite/tests/channel.json')
js = json.loads(test_channel)['packages_cache']['https://sublime.wbond.net/packages_2.json']


class TestRepository(unittest.TestCase):

    def setUp(self):
        pkgs = [repository.Package(x) for x in js]
        self.repo = repository.Repository(*pkgs)

    def test_empty_repo(self):
        repo = repository.Repository()
        self.assertEqual(0, len(repo.packages))

    def test_merge(self):
        repo = repository.Repository()
        repo.merge(self.repo)
        self.assertEqual(len(self.repo.packages), len(repo.packages))

    def test_get_package(self):
        name = 'SVN'

        p = self.repo.get_package(name)
        self.assertEqual(name, p.name)

        p = self.repo.get_package('not a package')
        self.assertFalse(p)

    def test_list(self):
        install_list = self.repo.list()

        self.assertIsInstance(install_list, list)

        packageOne = install_list[0]
        self.assertEqual('Alignment', packageOne[0])
        self.assertTrue('alignment' in packageOne[1])
        self.assertIn('2.1.0', packageOne[2])
