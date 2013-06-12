'''
The MIT License

Copyright (c) Bo Lopker, http://blopker.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

'''
Module to set the view status of Sublime Text plugins.
By @blopker
'''

from .lib.concurrent import futures
from . import logger
log = logger.get(__name__)
import time
import sublime

statusPool = futures.ThreadPoolExecutor(max_workers=1)
PLUGIN_NAME = 'PCLite'
# Default status display time in seconds
TIMEOUT = 10


def _get_current_view():
    window = sublime.active_window()
    view = window.active_view()
    return view


def _append_plugin_name(msg):
    return '%s: %s' % (PLUGIN_NAME, msg)


def _get_id(msg):
    return msg + str(time.time())


def _message_job(msg, seconds):
    view = _get_current_view()
    id = _get_id(msg)
    msg = _append_plugin_name(msg)
    view.set_status(id, msg)
    time.sleep(seconds)
    view.erase_status(id)


def message(msg, seconds=TIMEOUT):
    log.info(msg)
    statusPool.submit(_message_job, msg, seconds)


def error(msg, seconds=TIMEOUT):
    log.error(msg)
    msg = 'ERROR: ' + msg
    statusPool.submit(_message_job, msg, seconds)


def loading(msg):
    return Loader(msg)


class Loader(object):
    '''Class to start and cancel the status loading message.
    Call stop() on this object to remove the loading message.'''
    def __init__(self, message):
        self.message = message
        self.running = True
        statusPool.submit(self._show_progress, message)

    def _show_progress(self, msg):
        pos = 0
        # sym = ['-', '\\', '|', '/']
        loadingChars = '⣾⣽⣻⢿⡿⣟⣯⣷'
        view = _get_current_view()
        id = _get_id(msg)
        while self.running:
            stat = msg + ' [' + loadingChars[pos] + ']'
            stat = _append_plugin_name(stat)
            view.set_status(id, stat)
            pos = (pos + 3) % len(loadingChars)
            time.sleep(.1)
        view.erase_status(id)

    def stop(self):
        self.running = False
