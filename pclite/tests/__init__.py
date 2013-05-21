import imp
import unittest
from .. import settings

tests = ['test_install']

def run():
    for test in tests:
        name = __name__ + '.' + test
        unittest.main(module=name, argv=[""], exit=False)
        # Reset settings incase we changed anything during tests
        settings.init('PCLite.sublime-settings')
