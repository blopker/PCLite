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

from PCLite.pclite.lib import reloader

from PCLite.pclite import logger
log = logger.get(__name__)

from PCLite.pclite import commands
from PCLite.pclite import tests
from PCLite.pclite import settings
import sublime, sublime_plugin

# Tell modules to reload their dependancy trees now in a decorator!
def reload(module, debugOnly=True):
    def outer(func):
        def inner(*args, **kwargs):
            rld = (debugOnly and logger.isDebug()) or not debugOnly
            if rld:
                reloader.reload(module)
            return func(*args, **kwargs)
        return inner
    return outer


class PcliteInstallPackageCommand(sublime_plugin.WindowCommand):
    def run(self):
        print('Running install command.')
        commands.get_package_list(self.display_list)

    def display_list(self, lis):
        self.window.show_quick_panel(lis, self.on_select)

    def on_select(self, item):
        print(item)


# Also can run 'sublime.run_command('pclite_test')'
class PcliteTestCommand(sublime_plugin.ApplicationCommand):
    @reload(tests)
    def run(self):
        print('Running tests...')
        tests.run()


def plugin_loaded():
    reloader.enable()
    # Load dem settings
    settings.load('PCLite.sublime-settings')
    # Initialize the logger with this package's name
    logger.init(__name__, settings.get('debug', True))
    log.debug('PCLite loaded.')
