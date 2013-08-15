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
Global settings module for PCLite
By @blopker
'''
import sublime

PLUGIN_PREF = 'PCLite.sublime-settings'
SUBLIME_PREF = 'Preferences.sublime-settings'

pluginObj = {}
sublimeObj = {}


def load():
    global pluginObj
    pluginObj = sublime.load_settings(PLUGIN_PREF)

    global sublimeObj
    sublimeObj = sublime.load_settings(SUBLIME_PREF)
    # In case settings file is missing the debug value.
    debug = pluginObj.get('debug')
    if not debug:
        pluginObj.set('debug', True)


def get(*args):
    return pluginObj.get(*args)


def isDebug():
    return get('debug')


def platform():
    return sublime.platform()


def sublime_version():
    return int(sublime.version())


def add_package(package):
    pkgs = pluginObj.get('installed_packages', [])
    pkgs.append(package.name)
    pluginObj.set('installed_packages', pkgs)
    sublime.save_settings(PLUGIN_PREF)


def remove_package(package_name):
    pkgs = pluginObj.get('installed_packages', [])
    if package_name in pkgs:
        pkgs.remove(package_name)
    pluginObj.set('installed_packages', pkgs)
    sublime.save_settings(PLUGIN_PREF)


def ignore_package(package_name):
    ignored = sublimeObj.get('ignored_packages', [])
    if package_name not in ignored:
        ignored.append(package_name)
    sublimeObj.set('ignored_packages', ignored)
    sublime.save_settings(SUBLIME_PREF)


def unignore_package(package_name):
    ignored = sublimeObj.get('ignored_packages', [])
    if package_name in ignored:
        ignored.remove(package_name)
    sublimeObj.set('ignored_packages', ignored)
    sublime.save_settings(SUBLIME_PREF)
