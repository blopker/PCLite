from .. import settings


class Package(object):
    """docstring for Package"""
    def __init__(self, json):
        self.json = json
        dunno = 'Unknown'
        self.name = json.get('name', dunno)
        self.desc = json.get('description', dunno)
        self.supported = False

        releases = json.get('releases', [])
        release = self._get_release(releases)
        if not release:
            return

        self.supported = True
        self.version = release.get('version', '0.0.1')
        self.url = release.get('url', '')
        self.date = release.get('date', '2000-01-01 00:00:00')

    def _get_release(self, releases):
        for release in releases:
            plat = release.get('platform', ['*'])
            if not self._check_platform(plat):
                continue
            sub_ver = release.get('sublime_text', '*')
            if not self._check_sublime_version(sub_ver):
                continue
            return release
        return False

    def _check_platform(self, platforms):
        this_plat = settings.platform()
        if this_plat in platforms or '*' in platforms:
            return True
        return False

    def _check_sublime_version(self, version):
        if version == '*':
            return True
        ver = settings.sublime_version()
        try:
            num = int(version[-4:])
        except ValueError:
            return False
        op = version[:-4]
        if op == '>' and ver > num:
            return True
        if op == '>=' and ver >= num:
            return True
        if op == '<' and ver < num:
            return True
        if op == '<=' and ver <= num:
            return True
        return False

    def get_list(self):
        return [str(self.name), str(self.desc), str(self.version)]

    def is_supported(self):
        return self.supported
