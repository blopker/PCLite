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
import time

commandPool = futures.ThreadPoolExecutor(max_workers=10)
progressPool = futures.ThreadPoolExecutor(max_workers=1)


def _is_function(fn):
    return hasattr(fn, '__call__')


def _error(msg):
    return 'Command execution error: ' + msg


def command(fn):
    ''' Decorator for running commands asynchronously.
    Command functions should always have a callback as the
    first argument'''
    def wrap(*args, **kwargs):
        callback = ''
        try:
            callback = args[0]
        except IndexError:
            log.error(_error('No callback supplied.'))

        if not _is_function(callback):
            log.error(_error('%s is not a callback.', str(callback)))
            return

        def cb(fu):
            try:
                callback(fu.result())
            except Exception as e:
                log.error(_error('Failed with %s'), str(e))
                raise e
        commandFuture = commandPool.submit(fn, *args, **kwargs)
        commandFuture.add_done_callback(cb)
    return wrap


def run_command(fn, callback, *args, **kwargs):
    ''' Convenience function to run a command without the decorator. '''
    command(fn)(callback, *args, **kwargs)


@command
def get_package_list(callback):
    j = http.getJSON(settings.get('repositories')[0])
    return j["repositories"]


@command
def install_package(callback, packageRepo):
    return
