from .. import settings

def install_list(repositoryJSON):
    packages = repositoryJSON['packages']
    install_list = []
    for url, package_list in packages.items():
        for package in package_list:
            lis = _package_install_item(package)
            if lis:
                install_list.append(lis)
    return _sort_install_list(install_list)


def _package_install_item(itemDict):
    dunno = 'Unknown'
    name = itemDict.get('name', dunno)
    desc = itemDict.get('description', dunno)
    plat = settings.platform()
    opt = itemDict.get('platforms')
    if plat in opt:
        ver = opt[plat][0].get('version', dunno)
    elif '*' in opt:
        ver = opt['*'][0].get('version', dunno)
    else:
        return []
    return [str(name), str(desc), str(ver)]


def _sort_install_list(install_list):
    def compare(package_list):
        return package_list[0].capitalize()
    return sorted(install_list, key=compare)
