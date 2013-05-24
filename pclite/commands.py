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

from . import logger
log = logger.get(__name__)
from . import settings
from . import http
from .lib.concurrent import futures
import sublime
import time

commandPool = futures.ThreadPoolExecutor(max_workers=10)
progressPool = futures.ThreadPoolExecutor(max_workers=1)


def command(message='Processing'):
    ''' Decorator for running commands in the command thread pool.
    This decorator takes a message that will be displayed with a
    progress meter as the command executes.
    '''
    def outer(fn):
        def wrap(*args, **kwargs):
            callback = args[0]
            running = [True]

            def show_progress(msg):
                pos = 0
                # sym = ['-', '\\', '|', '/']
                sym = '⣾⣽⣻⢿⡿⣟⣯⣷'
                window = sublime.active_window()
                view = window.active_view()
                while running[0] is True:
                    view = window.active_view()
                    stat = msg + ' [' + sym[pos] + ']'
                    view.set_status(msg, stat)
                    pos = (pos + 3) % len(sym)
                    time.sleep(.1)
                view.erase_status(msg)

            progressPool.submit(show_progress, message)

            def cb(fu):
                try:
                    running[0] = False
                    callback(fu.result())
                except Exception as e:
                    raise e
            commandFuture = commandPool.submit(fn, *args, **kwargs)
            commandFuture.add_done_callback(cb)
        return wrap
    return outer


def run_command(message, fn, callback, *args, **kwargs):
    ''' Convenience function to run a command without the decorator. '''
    command(message)(fn)(callback, *args, **kwargs)


@command('Getting package list')
def get_package_list(callback):
    j = http.getJSON(settings.get('repositories')[0])
    return j["repositories"]


@command('Installing package')
def install_package(packageRepo):
    return
