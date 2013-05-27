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
from . import io
from .lib.concurrent import futures
from .models import Repository

commandPool = futures.ThreadPoolExecutor(max_workers=10)
progressPool = futures.ThreadPoolExecutor(max_workers=1)


def _is_function(fn):
    return hasattr(fn, '__call__')


def _error(msg):
    return 'Command execution error: ' + msg


def command(fn):
    ''' Decorator for running commands asynchronously.
    Command functions can have a callback as the
    last argument'''
    def wrap(*args):
        callback = False
        if len(args) > 0 and _is_function(args[-1]):
            callback = args[-1]

        def cb(future):
            try:
                result = future.result()
            except Exception as e:
                log.error(_error('Failed with %s'), str(e))
                callback(False)
                raise e
            else:
                callback(result)

        commandFuture = commandPool.submit(fn, *args)
        if callback:
            commandFuture.add_done_callback(cb)
    return wrap


@command
def get_repository(callback):
    # Get all the repositories
    repos = []
    urls = settings.get('repositories', [])
    for url in urls:
        j = http.getJSON(url)
        if j:
            repos.append(Repository(j))

    # Merge into one repo
    repo = Repository()
    for r in repos:
        repo.merge(r)

    if len(repo.packages) is 0:
        return False
    return repo


@command
def install_package(package_name, repository, callback):
    try:
        p = repository.get_package(package_name)
        if not p:
            return False
        zip_data = http.get_zip(p.url)
        if not zip_data:
            return False
        return io.install_zip(p, zip_data)
    except Exception:
        return False
