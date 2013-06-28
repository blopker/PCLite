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
