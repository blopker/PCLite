import unittest
from .. import commands


class TestSequenceFunctions(unittest.TestCase):

    def test_package_list(self):
        self.assertEqual(self.seq, list(range(10)))

    def test_set(self):
        self.assertEqual(self.set, set(range(10)))
