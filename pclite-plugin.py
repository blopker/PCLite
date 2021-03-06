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

from PCLite.pclite import commands
from PCLite.pclite import status
import sublime_plugin

NO_SELECTION = -1


class PcliteInstallPackageCommand(sublime_plugin.WindowCommand):
    def run(self):
        print('Running install command.')
        self.status = status.loading('Getting package list')
        commands.get_repository(self.display_list)

    def display_list(self, repo):
        self.status.stop()
        if not repo:
            status.error('Package list not found. Please check internet ' +
                         'connection or enable debug in the settings and ' +
                         'report the stack traces.')
            return
        self.repo = repo
        self.list = repo.list()
        self.window.show_quick_panel(self.list, self.on_select)

    def on_select(self, item_idx):
        if item_idx is NO_SELECTION:
            status.message('Package install canceled.')
            return
        p = self.list[item_idx][0]
        self.status = status.loading('Installing package: %s' % p)
        commands.install_package(p, self.repo, self.install_success)

    def install_success(self, success):
        self.status.stop()
        if success:
            status.message('Package installed successfully!')
        else:
            status.error('Package install was unsuccessful. Please check console.')


class PcliteRemovePackageCommand(sublime_plugin.WindowCommand):
    def run(self):
        print('Running remove command.')
        self.status = status.loading('Getting installed package list')
        commands.get_installed(self.display_list)

    def display_list(self, installed):
        self.status.stop()
        if not installed:
            status.error('No packages installed! Please install some first.')
            return
        self.list = installed
        self.window.show_quick_panel(self.list, self.on_select)

    def on_select(self, item_idx):
        if item_idx is NO_SELECTION:
            return
        p = self.list[item_idx]
        self.status = status.loading('Removing package: %s' % p)
        commands.remove_package(p, self.remove_success)

    def remove_success(self, success):
        self.status.stop()
        if success:
            status.message('Package removed.')
        else:
            status.error('Package removal was unsuccessful.')


class PcliteUpdatePackageCommand(sublime_plugin.WindowCommand):
    def run(self):
        print('Running update command.')
        self.status = status.loading('Getting installed package list')
        commands.get_installed(self.display_list)

    def display_list(self, installed):
        self.status.stop()
        if not installed:
            status.error('No packages installed! Please install some first.')
            return
        allPackage = 'Update all packages'
        self.list = [allPackage]
        self.list.extend(installed)
        print(self.list)
        self.window.show_quick_panel(self.list, self.on_select)

    def on_select(self, item_idx):
        if item_idx is NO_SELECTION:
            return
        p = self.list[item_idx]
        self.status = status.loading('Removing package: %s' % p)
        commands.remove_package(p, self.remove_success)

    def remove_success(self, success):
        self.status.stop()
        if success:
            status.message('Package removed.')
        else:
            status.error('Package removal was unsuccessful.')
