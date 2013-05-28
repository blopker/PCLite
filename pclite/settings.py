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
Global settings module for Sublime Test plugins
By @blopker
'''
import sublime

FILE_NAME = 'PCLite.sublime-settings'

settingsObj = {}


def load():
    global settingsObj
    settingsObj = sublime.load_settings(FILE_NAME)
    # In case settings file is missing the debug value.
    debug = settingsObj.get('debug')
    if not debug:
        settingsObj.set('debug', debug)


def get(*args):
    return settingsObj.get(*args)


def isDebug():
    return get('debug')


def platform():
    return sublime.platform()


def add_package(package):
    pkgs = settingsObj.get('installed_packages', [])
    pkgs.append(package.name)
    settingsObj.set('installed_packages', pkgs)
    sublime.save_settings(FILE_NAME)


def remove_package(package_name):
    pkgs = settingsObj.get('installed_packages', [])
    if package_name in pkgs:
        pkgs.remove(package_name)
    settingsObj.set('installed_packages', pkgs)
    sublime.save_settings(FILE_NAME)
