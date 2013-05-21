from .lib import requests
from . import settings
import time


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


@cache
def get(url):
    r = requests.get(url)
    return r.content


@cache
def getJSON(jsonURL):
    r = requests.get(jsonURL)
    return r.json()
