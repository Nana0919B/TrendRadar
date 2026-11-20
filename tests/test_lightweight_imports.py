"""Collection and storage must work without importing AI/AppContext."""

import subprocess
import sys
import unittest


class LightweightImportsTests(unittest.TestCase):
    def test_collectors_do_not_import_context_or_ai(self):
        subprocess.run([sys.executable, "-c", """
import importlib.abc
import sys
class NoAI(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'trendradar.context' or fullname.startswith('trendradar.ai'):
            raise AssertionError('Unexpected AI import: ' + fullname)
sys.meta_path.insert(0, NoAI())
from trendradar.crawler import DataFetcher
from trendradar.storage import LocalStorageBackend
from trendradar.crawler.rss import RSSFetcher
assert 'litellm' not in sys.modules
"""], check=True)

    def test_public_app_context_export_remains_available_lazily(self):
        subprocess.run([sys.executable, "-c", """
import sys
import types
import trendradar
assert 'trendradar.context' not in sys.modules
stub = types.ModuleType('trendradar.context')
stub.AppContext = type('AppContext', (), {})
sys.modules['trendradar.context'] = stub
from trendradar import AppContext
assert AppContext is stub.AppContext
assert trendradar.AppContext is AppContext
try:
    trendradar.missing_attribute
except AttributeError:
    pass
else:
    raise AssertionError('Missing attribute must raise')
"""], check=True)


if __name__ == "__main__":
    unittest.main()
