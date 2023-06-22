import importlib
import os
from datetime import date
from unittest import TestCase
from unittest.mock import patch

import paths


class TestPaths(TestCase):
    def setUp(self):
        # Force the paths module to reload to get the patches
        # otherwise the patches take no effect because methods in paths are cahced
        importlib.reload(paths)

    @patch("paths.BASE_PATH", "base")
    def test_snippet_path(self):
        want = os.path.join("base", "src", "1994", "1", "1", "hello")
        got = paths.snippet_path("hello", date(1994, 1, 1))
        self.assertEqual(got, want)

    def test_rel(self):
        cases = [
            (os.path.join("base"), os.path.join("base", "1", "2"), "../.."),
            (os.path.join("base", "1", "2"), os.path.join("base"), "1/2"),
            (os.path.join("base", "1", "2"), os.path.join("base", "3", "4"), "../../1/2")
        ]
        for path, start, expected in cases:
            self.assertEqual(expected, paths.rel(path, start))
