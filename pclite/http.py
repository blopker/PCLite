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
Abstraction for the HTTP layer.
By @blopker
'''

from .lib import requests
from . import settings
import time

# Check if this OS supports SSL
try:
    import ssl
except ImportError:
    SSL = False
else:
    SSL = True


def cache(fn):
    ''' A decorator to cache method invocation.
    Cache expires after a set time.
    '''
    cacheDB = {}

    def isCached(args):
        if args in cacheDB:
            cache_time = settings.get('cache_time', 0)
            age = time.time() - cacheDB[args][0]
            if age < cache_time:
                return True
        return False

    def putCache(args, ans):
        cacheDB[args] = (time.time(), ans)

    def getCache(args):
        return cacheDB[args][1]

    def wrap(*args):
        if isCached(args):
            return getCache(args)
        else:
            ans = fn(*args)
            putCache(args, ans)
            return ans
    return wrap


# Changes URL based on environment
def _fixURL(url):
    if not SSL:
        url = url.replace('https://', 'http://')
    return url


@cache
def get(url):
    url = _fixURL(url)
    try:
        r = requests.get(url).content
    except ConnectionError:
        r = False
    return r


@cache
def getJSON(jsonURL):
    jsonURL = _fixURL(jsonURL)
    try:
        r = requests.get(jsonURL).json()
    except ConnectionError:
        r = False
    return r


@cache
def get_zip(zipurl):
    zipurl = _fixURL(zipurl)
    try:
        r = requests.get(zipurl).content
    except ConnectionError:
        r = False
    return r
