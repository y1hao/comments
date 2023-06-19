import importlib
import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

import paths
import snippets


class TestSnippets(TestCase):
    def setUp(self):
        # Force the paths module to reload to get the patches
        # otherwise the patches take no effect because methods in paths are cahced
        importlib.reload(paths)

    @patch("paths.BASE_PATH", os.path.join("scripts", "test_files", "snippet_test"))
    def test_get_all(self: TestCase):
        expected = [
            snippets.Snippet("Test Snippet 1", "Summary 1", datetime(2023, 6, 19), frozenset(), "test_snippet_1", False),
            snippets.Snippet("Test Snippet 2", "", datetime(2023, 6, 19), frozenset(["draft", "random"]), "test_snippet_2", True),
            snippets.Snippet("Test Snippet 3", "Summary 3", datetime(2023, 6, 20), frozenset(), "test_snippet_3", False)
        ]

        got = list(snippets.get_all())

        self.assertEqual(set(got), set(expected))
        
