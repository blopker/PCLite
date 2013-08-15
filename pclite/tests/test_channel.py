import unittest
import sublime
from .. import repository
import json

txt = sublime.load_resource('Packages/PCLite/pclite/tests/channel.json')
js = json.loads(txt)


class TestChannel(unittest.TestCase):

    def setUp(self):
        self.channel = repository.Channel(js)
        self.url = "https://sublime.wbond.net/packages_2.json"

    def test_urls(self):
        self.assertTrue(self.url in self.channel.urls())
        self.assertTrue('notaurl' not in self.channel.urls())

    def test_cache(self):
        self.assertTrue(self.channel.get_cache(self.url) is not False)
        self.assertTrue(self.channel.get_cache('notaurl') is False)
