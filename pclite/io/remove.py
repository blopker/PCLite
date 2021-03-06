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

import os
import traceback
import sublime
import time

from .. import logger
log = logger.get(__name__)
from .. import settings
from . import util


def remove_package(package_name):
    settings.ignore_package(package_name)
    pkg = package_name + util.PKG_SUFFIX
    pkg_path = os.path.join(sublime.installed_packages_path(), pkg)
    try:
        os.remove(pkg_path)
        success = True
    except PermissionError:
        log.error('Permission error.')
        traceback.print_exc()
        success = False
    except:
        log.error('Package %s does not exist on file system.', package_name)
        traceback.print_exc()
        success = False
    # Take a nap so ST has time to catch up. May cause exception otherwise.
    time.sleep(0.5)
    settings.unignore_package(package_name)
    return success
