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
Collection of functions the PCLite plugin can invoke. Most if not all should be
non-blocking (@async) functions to keep the main UI thread from freezing.

These functions should catch all unexpected exceptions so the plugin does not
have to. Unexpected exceptions should return False. Expected exceptions should
be caught by other modules this module uses. Log all unusual behavior.

All @async functions have an optional callback parameter as the last argument.
'''

from . import logger
log = logger.get(__name__)
from . import settings
from . import http
from . import io
from .async import async
from .models import Repository
import traceback


@async
def get_repository():
    try:
        # Get all the repositories
        repos = []
        urls = settings.get('repositories', [])
        for url in urls:
            try:
                j = http.get_json(url)
                if j:
                    repos.append(Repository(j))
            except:
                log.warning('Unable to fetch repository at %s', url)

        # Merge into one repo
        repo = Repository()
        for r in repos:
            repo.merge(r)

        if len(repo.packages) is 0:
            log.error('No packages found.')
            return False

        return repo
    except:
        log.error('Unable to get repository for unknown reason:')
        traceback.print_exc()
    return False


@async
def install_package(package_name, repository):
    try:
        p = repository.get_package(package_name)
        if not p:
            log.error('Unable to find package %s in repository.', package_name)
            return False
        zip_data = http.get_file(p.url)
        if not zip_data:
            log.error('Unable get package %s from internet. Please check connection.', p.name)
            return False
        if not io.install_package(p, zip_data):
            log.error('Unable to install package %s because of IO issues.', p.name)
            return False
        settings.add_package(p)
        return True
    except:
        log.error('Unable to install package for unknown reason:')
        traceback.print_exc()
    return False


@async
def get_installed():
    return settings.get('installed_packages')


@async
def remove_package(package_name):
    try:
        settings.remove_package(package_name)
        if not io.remove_package(package_name):
            return 'Package %s does not exist! No need to remove.' % package_name
        return 'Package %s removed.' % package_name
    except:
        log.error('Unable to remove package for unknown reason:')
        traceback.print_exc()
    return False
