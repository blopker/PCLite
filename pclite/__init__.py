from . import logger
log = logger.get(__name__)
from . import settings


def plugin_loaded():
    # Load dem settings
    settings.load('PCLite.sublime-settings')
    # Initialize the logger with this package's name
    logger.init(__name__, settings.get('debug', True))
    log.debug('PCLite loaded.')
