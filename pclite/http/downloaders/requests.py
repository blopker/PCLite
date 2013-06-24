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
from .downloader_base import DownloaderBase
from ...lib import requests as req
from ... import logger
log = logger.get(__name__)
import traceback


class RequestsDownloader(DownloaderBase):
    """Downloader that uses the Requests library."""
    def get(self, url):
        try:
            log.debug('Requests downloader getting url %s', url)
            return req.get(url)
        except TypeError:
            log.error('This platform does not support SSL with the Requests downloader.')
            traceback.print_exc()
        return False

    def get_json(self, url):
        a = self.get(url)
        if a:
            try:
                a = a.json()
            except ValueError:
                log.error('URL %s does not contain a JSON file.', url)
                return False
        return a

    def get_file(self, url):
        a = self.get(url)
        if a:
            a = a.content
        return a
