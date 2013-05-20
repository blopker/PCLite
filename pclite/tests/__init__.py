import imp
import unittest

tests = ['test_install']

def run():
    for test in tests:
        name = __name__ + '.' + test
        unittest.main(module=name, argv=[""], exit=False)

