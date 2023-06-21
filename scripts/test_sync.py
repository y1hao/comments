import importlib
import os
import shutil
from unittest import TestCase
from unittest.mock import patch

import paths
import sync


class TestSync(TestCase):
    def setUp(self):
        # Force the paths module to reload to get the patches
        # otherwise the patches take no effect because methods in paths are cahced
        importlib.reload(paths)

    @patch("paths.BASE_PATH", os.path.join("scripts", "test_files", "sync_test"))
    @patch("sync.PAGE_SIZE", 2)
    def test_sync(self: TestCase):
        base = os.path.join("scripts", "test_files", "sync_test")
        try:
            sync.sync()
            self.assertTrue(os.path.exists(os.path.join(base, "README.md")))
            self.assertTrue(os.path.exists(os.path.join(base, "index", "archive.md")))
            self.assertTrue(os.path.exists(os.path.join(base, "index", "tags.md")))
            self.assertTrue(os.path.exists(os.path.join(base, "index", "pages")))
            for i in [1, 2]:
                self.assertTrue(os.path.exists(os.path.join(base, "index", "pages", f"{i}.md")))
        finally:
            if os.path.exists(os.path.join(base, "index")):
                shutil.rmtree(os.path.join(base, "index"))
            if os.path.exists(os.path.join(base, "README.md")):
                os.remove(os.path.join(base, "README.md"))