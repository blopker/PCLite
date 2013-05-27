from itertools import chain
from .. import settings


class Package(object):
    """docstring for Package"""
    def __init__(self, json):
        self.json = json
        dunno = 'Unknown'
        self.name = json.get('name', dunno)
        self.desc = json.get('description', dunno)
        self.supported = True

        plat = settings.platform()
        opt = json.get('platforms')
        if plat in opt:
            platData = opt[plat][0]
        elif '*' in opt:
            platData = opt['*'][0]
        else:
            platData = {}
            self.supported = False

        self.version = platData.get('version', dunno)
        self.url = platData.get('url', dunno)

    def get_list(self):
        return [str(self.name), str(self.desc), str(self.version)]

    def is_supported(self):
        return self.supported


class Repository(object):
    """docstring for Repository"""
    def __init__(self, json={}):
        self.packages = {}
        if not json:
            return
        self._create_packages(json)

    def _create_packages(self, json):
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

    def install_list(self):
        install_list = []
        for package in self.packages.values():
            install_list.append(package.get_list())
        return self._sort_package_list(install_list)

    def merge(self, repository):
        self.packages.update(repository.packages)
        return self

    def get_package(self, name):
        return self.packages.get(name, False)
