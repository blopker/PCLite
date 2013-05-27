import unittest
from .. import io
from collections import namedtuple
import os
import sublime
from zipfile import ZipFile

Package = namedtuple('Package', 'name')


class TestIO(unittest.TestCase):

    def setUp(self):
        self.inst_path = sublime.installed_packages_path()

    def _get_zip_data(self):
        root = __file__.rpartition(os.sep)[0]
        zip_path = os.path.join(root, 'test.zip')
        f = open(zip_path, 'rb')
        zip_data = f.read()
        f.close()
        return zip_data

    def test_install_zip(self):
        pname = 'test-package'
        pzip = pname + '.sublime-package'
        ppath = os.path.join(self.inst_path, pzip)
        p = Package(pname)
        success = io.install_zip(p, self._get_zip_data())

        self.assertTrue(success)
        self.assertTrue(os.path.exists(ppath))
        with ZipFile(ppath, 'r') as z:
            self.assertIsNone(z.testzip())
            self.assertIn('test.py', z.namelist())

        os.remove(ppath)
