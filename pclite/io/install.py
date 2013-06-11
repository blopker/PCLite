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

from zipfile import ZipFile
import traceback
import tempfile
import shutil
import os
import sublime
from .. import logger
log = logger.get(__name__)
from . import util
from .. import settings


def _zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            loc = os.path.join(root, file)
            # Make sure plugin files are at root
            arcname = os.path.relpath(loc, start=path)
            zip.write(loc, arcname=arcname)


def _make_zip_file(data):
    try:
        zh, zip_file = tempfile.mkstemp()
        with open(zip_file, 'wb') as f:
            f.write(data)
        result = zip_file
    except:
        log.error('Zip creation failed.')
        traceback.print_exc()
        result = False
    finally:
        os.close(zh)
    return result


def install_package(package, zip_data):
    settings.ignore_package(package.name)
    result = True
    try:
        zip_file = _make_zip_file(zip_data)
        if not zip_file:
            return False

        prefix = ''

        tmp_dir = tempfile.mkdtemp()

        # Extract files from zip data
        with ZipFile(zip_file, 'r') as myzip:
            prefix = os.path.commonprefix(myzip.namelist())
            myzip.extractall(path=tmp_dir)

        # Repackage with correct name, location and folder tree
        pkg = package.name + util.PKG_SUFFIX
        install_path = os.path.join(sublime.installed_packages_path(), pkg)
        with ZipFile(install_path, 'w') as myzip:
            _zipdir(os.path.join(tmp_dir, prefix), myzip)

    except PermissionError:
        log.error('Permission error.')
        traceback.print_exc()
        result = False
    except:
        log.error('Unexpected exception:')
        traceback.print_exc()
        result = False
    finally:
        shutil.rmtree(tmp_dir)
        os.remove(zip_file)
        settings.unignore_package(package.name)
    return result
