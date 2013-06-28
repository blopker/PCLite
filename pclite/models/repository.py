from itertools import chain
from .package import Package


class Repository(object):
    """docstring for Repository"""
    def __init__(self, json={}):
        self.packages = {}
        if not json:
            return
        self._add_packages(json)

    def _add_packages(self, json):
        packages = {}
        for p in chain(*json['packages'].values()):
            package = Package(p)
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
