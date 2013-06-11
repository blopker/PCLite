import unittest
from .. import io
from collections import namedtuple
import os
import sublime
from zipfile import ZipFile

Package = namedtuple('Package', 'name')
TEST_DIR = 'Packages/PCLite/pclite/tests/'


class TestIO(unittest.TestCase):

    def setUp(self):
        self.inst_path = sublime.installed_packages_path()

    def _get_zip_data(self):
        zip_data = sublime.load_binary_resource(TEST_DIR + 'test.zip')
        return zip_data

    def test_install_remove_zip(self):
        pname = 'test-package'
        pzip = pname + '.sublime-package'
        ppath = os.path.join(self.inst_path, pzip)
        p = Package(pname)
        success = io.install_package(p, self._get_zip_data())

        self.assertTrue(success)
        self.assertTrue(os.path.exists(ppath))
        with ZipFile(ppath, 'r') as z:
            self.assertIsNone(z.testzip())
            self.assertIn('test.py', z.namelist())

        success = io.remove_package(pname)
        self.assertTrue(success)
        self.assertFalse(os.path.exists(ppath))
