import unittest


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))
        self.set = set(range(10))

    def test_list(self):
        self.assertEqual(self.seq, list(range(10)))

    def test_set(self):
        self.assertEqual(self.set, set(range(10)))
