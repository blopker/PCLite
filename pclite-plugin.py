from PCLite.pclite import logger, commands
from PCLite.pclite import tests
log = logger.get(__name__)
import sublime, sublime_plugin
import imp

class PcliteInstallPackageCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print('Running install command.')
        lis = commands.get_package_list()
        print(lis)
        # r = requests.get("http://blopker.com")
        # self.view.insert(edit, 0, r.text)

# Also can run 'sublime.run_command('pclite_test')'
class PcliteTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        print('Running tests...')
        imp.reload(tests)
        tests.run()
