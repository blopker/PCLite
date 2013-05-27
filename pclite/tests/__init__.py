import unittest
from .. import settings
from .. import logger
log = logger.get(__name__)

tests = ['test_repository', 'test_io']


def run():
    for test in tests:
        log.debug('Running test: %s' % test)
        name = __name__ + '.' + test
        unittest.main(module=name, argv=[""], exit=False)
        # Reset settings in case we changed anything during tests
        settings.load('PCLite.sublime-settings')
