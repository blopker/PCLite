from .lib import requests

def get_package_list():
    r = requests.get('http://sublime.wbond.net/repositories.json')
    return r.content
