from .lib.concurrent import futures
from . import logger
log = logger.get(__name__)
import random
import time
import sublime

statusPool = futures.ThreadPoolExecutor(max_workers=1)


def message(msg, seconds=5):
    if not msg:
        return
    log.info(msg)
    statusPool.submit(_message_job, msg, seconds)


def _message_job(msg, seconds):
    window = sublime.active_window()
    view = window.active_view()
    msg = 'PCLite: ' + msg
    view.set_status(msg, msg)
    time.sleep(seconds)
    view.erase_status(msg)


def loading(msg):
    return Loader(msg)


class Loader(object):
    """Class to start and cancel the status loading message."""
    def __init__(self, message):
        self.message = message
        self.running = True
        statusPool.submit(self._show_progress, message)

    def _show_progress(self, msg):
        # Pick a random range for the message ID
        r = str(random.randrange(0, 1000))
        pos = 0
        # sym = ['-', '\\', '|', '/']
        sym = '⣾⣽⣻⢿⡿⣟⣯⣷'
        window = sublime.active_window()
        view = window.active_view()
        while self.running:
            view = window.active_view()
            stat = msg + ' [' + sym[pos] + ']'
            stat = 'PCLite: ' + stat
            view.set_status(r, stat)
            pos = (pos + 3) % len(sym)
            time.sleep(.1)
        view.erase_status(msg)

    def cancel(self):
        self.running = False
