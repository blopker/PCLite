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


class Repository(object):
    """docstring for Repository"""
    def __init__(self, *args):
        self.packages = {}
        for package in args:
            try:
                self._add_package(package)
            except AttributeError:
                continue

    def _add_package(self, package):
        packages = {}
        if package.is_supported():
            packages[package.name] = package
        self.packages.update(packages)

    def _sort_package_list(self, package_list):
        def compare(lis):
            return lis[0].upper()
        return sorted(package_list, key=compare)

    def list(self):
        install_list = []
        for package in self.packages.values():
            install_list.append(package.get_list())
        return self._sort_package_list(install_list)

    def merge(self, repository):
        self.packages.update(repository.packages)
        return self

    def get_package(self, name):
        return self.packages.get(name, False)
