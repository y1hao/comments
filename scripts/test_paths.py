import importlib
import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

import paths


class TestPaths(TestCase):
    def setUp(self):
        # Force the paths module to reload to get the patches
        # otherwise the patches take no effect because methods in paths are cahced
        importlib.reload(paths)

    @patch("paths.BASE_PATH", "base")
    @patch("paths.DATE", datetime(1994, 1, 1))
    def test_snippet_path(self: TestCase):
        want = os.path.join("base", "src", "1994", "1", "1", "hello")
        got = paths.snippet_path("hello")
        self.assertEqual(got, want)
