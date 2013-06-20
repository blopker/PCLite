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
from .. import settings
import time


def cache(fn):
    ''' A decorator to cache method invocation.
    Cache expires after a set time.
    '''
    cacheDB = {}

    def putCache(args, ans):
        # Disable cache for debug.
        if settings.isDebug():
            return

        if ans:
            cacheDB[args] = (time.time(), ans)

    def getCache(args):
        # Disable cache for debug.
        if settings.isDebug():
            return []

        # Get result while cleaning old cache.
        t = time.time()
        cache_time = settings.get('cache_time', 0)
        ans = False
        for c in cacheDB:
            age = t - cacheDB[c][0]
            if age > cache_time:
                del cacheDB[c]
                continue
            if c == args:
                ans = cacheDB[args][1]
        return ans

    def wrap(*args):
        ans = getCache(args)
        if ans is False:
            ans = fn(*args)
            putCache(args, ans)
        return ans
    return wrap
