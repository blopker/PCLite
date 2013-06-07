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
Decorator to run functions asynchronously.
'''
from .lib.concurrent import futures
from . import logger
log = logger.get(__name__)
asyncPool = futures.ThreadPoolExecutor(max_workers=10)


def _is_function(fn):
    return hasattr(fn, '__call__')


def _error(msg):
    return 'Command execution error: ' + msg


def async(fn):
    ''' Decorator for running functions asynchronously.
    Async functions can have a callback as the
    last argument.

    e.x. no callback:
    @async
    def no_callback(arg):
        chage_some_state(arg)

    no_callback(2)

    or has callback:
    @async
    def has_callback(arg):
        return arg*2

    has_callback(2, callback)
    '''
    def wrap(*args):
        callback = False
        if len(args) > 0 and _is_function(args[-1]):
            callback = args[-1]
            args = args[:-1]

        def cb(future):
            try:
                result = future.result()
            except Exception as e:
                log.error(_error('Failed with %s'), str(e))
                callback(False)
                raise e
            else:
                callback(result)

        asyncFuture = asyncPool.submit(fn, *args)
        if callback:
            asyncFuture.add_done_callback(cb)
    return wrap
