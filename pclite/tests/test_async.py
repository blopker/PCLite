import unittest
from .. import async


class TestAsync(unittest.TestCase):

    def test_async_map(self):
        args = [max, [1, 3, 6], [2, 2, 7]]
        a = async.asyncMap(*args)
        b = [x for x in map(*args)]
        self.assertEqual(a, b)
