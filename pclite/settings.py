import sublime

settingsObj = {}

def load(filename):
    global settingsObj
    settingsObj = sublime.load_settings(filename)
    settingsObj.set('debug', True)

def get(*args):
    return settingsObj.get(*args)
