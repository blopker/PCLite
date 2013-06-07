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
from .async import async
from .models import Repository


@async
def get_repository():
    # Get all the repositories
    repos = []
    urls = settings.get('repositories', [])
    for url in urls:
        j = http.get_json(url)
        if j:
            repos.append(Repository(j))

    # Merge into one repo
    repo = Repository()
    for r in repos:
        repo.merge(r)

    if len(repo.packages) is 0:
        return False
    return repo


@async
def install_package(package_name, repository):
    try:
        p = repository.get_package(package_name)
        if not p:
            return 'Unable to get repository.'
        zip_data = http.get_file(p.url)
        if not zip_data:
            return 'Unable get package %s.' % p.name
        if not io.install_zip(p, zip_data):
            return 'Unable to install package.'
        settings.add_package(p)
        return '%s installed successfully!' % p.name
    except:
        return False


@async
def get_installed():
    return settings.get('installed_packages')


@async
def remove_package(package_name):
    settings.remove_package(package_name)
    if io.remove_zip(package_name):
        return "Package removed!"
    return False
