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
from ... import logger
log = logger.get(__name__)
import traceback
import subprocess
import json
import shutil


def is_available():
    if shutil.which('wget'):
        return True
    return False


class WgetDownloader(DownloaderBase):
    """Downloader that uses the command line program wget."""
    def get(self, url):
        try:
            log.debug('Wget downloader getting url %s', url)
            result = subprocess.check_output(['wget', '-qO-', url])
        except subprocess.CalledProcessError:
            log.error('Wget downloader failed.')
            traceback.print_exc()
            result = False
        return result

    def get_json(self, url):
        a = self.get(url)
        if a:
            try:
                a = json.loads(a.decode('utf-8'))
            except ValueError:
                log.error('URL %s does not contain a JSON file.', url)
                return False
        return a

    def get_file(self, url):
        return self.get(url)
