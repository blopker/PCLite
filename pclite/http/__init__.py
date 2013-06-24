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
from .cache import cache
from . import downloaders
from .. import logger
log = logger.get(__name__)
import sys
import traceback

downloader = downloaders.get()


@cache
def get(url):
    return _run_downloader(downloader.get, url)


@cache
def get_json(url):
    return _run_downloader(downloader.get_json, url)


@cache
def get_file(url):
    return _run_downloader(downloader.get_file, url)


def _run_downloader(fn, url):
    try:
        log.debug('HTTP url %s with function %s', url, fn.__name__)
        return fn(url)
    except NotImplementedError:
        log.error('Function %s not implemented in downloader %s.',
                  fn.__name__, downloader.__class__.__name__)
    except AttributeError as e:
        log.error(e)
        traceback.print_exc()
    except:
        log.error('Unexpected exception: %s', sys.exc_info()[0])
        traceback.print_exc()
    return False
