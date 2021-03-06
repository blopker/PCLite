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
Module to determine the correct downloader to use.
By @blopker
'''
from . import requests
from . import null
from . import wget
from ... import logger
log = logger.get(__name__)

# Check if this OS supports SSL
try:
    import ssl
    SSL = True
except ImportError:
    SSL = False


def get():
    if not SSL and wget.is_available():
        log.debug('Using WGET downloader.')
        return wget.WgetDownloader()
    if SSL:
        log.debug('Using Requests downloader.')
        return requests.RequestsDownloader()
    log.error('No suitable downloader found. Everything is terrible.')
    return null.NullDownloader()
