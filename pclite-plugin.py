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

from PCLite.pclite import logger
log = logger.get(__name__)

from PCLite.pclite import commands
from PCLite.pclite import status
import sublime_plugin


class PcliteInstallPackageCommand(sublime_plugin.WindowCommand):
    def run(self):
        print('Running install command.')
        self.status = status.loading('Getting package list')
        commands.get_package_list(self.display_list)

    def display_list(self, lis):
        self.status.stop()
        if not lis:
            status.message('Package list not found. Please check internet connection.')
            return
        self.package_list = lis
        self.window.show_quick_panel(lis, self.on_select)

    def on_select(self, item_idx):
        if item_idx is -1:
            return
        commands.install_package(self.package_list[item_idx])
