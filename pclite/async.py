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
import traceback
from .lib.concurrent import futures
from . import logger
log = logger.get(__name__)
from . import settings
asyncPool = futures.ThreadPoolExecutor(max_workers=10)


def _is_function(fn):
    return hasattr(fn, '__call__')


def async(fn):
    ''' Decorator for running functions asynchronously.
    Async functions can have a callback as the
    last argument. Returns False if uncaught exception.

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
                callback(result)
            except:
                log.error('Command execution error:')
                traceback.print_exc()
                callback(False)
            return

        asyncFuture = asyncPool.submit(fn, *args)
        if callback:
            asyncFuture.add_done_callback(cb)
    return wrap


def asyncMap(fn, *args):
    ''' A method that emulates Python's built-in map(),
    but each function call is done in async.
    asyncMap() blocks until all functions have finished.
    Returns a list of results. If a function call times out
    or raises an exception that result will be False.

    e.x.
    >>> asyncMap(max, [1,3,6], [2,2,7])
    [2,3,7]
    '''

    timeout = settings.get('http_timeout', 10) + 5
    calls = max([len(x) for x in args])
    results = []
    with futures.ThreadPoolExecutor(max_workers=10) as exe:
        maps = exe.map(fn, *args, timeout=timeout)
        for i in range(calls):
            try:
                results.append(maps.__next__())
            except:
                results.append(False)
                traceback.print_exc()

    return results
