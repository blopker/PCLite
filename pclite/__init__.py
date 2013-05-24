from . import logger
from . import settings
from . import tests
log = logger.get(__name__)


def run_tests():
    print('Running PCLite tests...')
    tests.run()


def plugin_loaded():
    # Load dem settings
    settings.load('PCLite.sublime-settings')
    # Initialize the logger with this package's name
    logger.init(__name__, settings.get('debug', True))
    if logger.isDebug():
        run_tests()
    log.debug('PCLite loaded.')
