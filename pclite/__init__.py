from . import logger
from . import settings
from . import tests
log = logger.get(__name__)


def run_tests():
    log.debug('Running PCLite tests...')
    tests.run()


def plugin_loaded():
    # Load dem settings
    settings.load()
    # Initialize the logger with this package's root name
    logger.init(__name__, settings.get('debug'))
    if settings.get('run_tests'):
        run_tests()
    log.debug('Loaded.')
