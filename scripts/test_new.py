import importlib
import os
import shutil
from datetime import date
from unittest import TestCase
from unittest.mock import patch

import new
import paths


class TestNew(TestCase):
    def setUp(self):
        # Force the paths module to reload to get the patches
        # otherwise the patches take no effect because methods in paths are cahced
        importlib.reload(paths)

    @patch("paths.BASE_PATH", "test_base")
    @patch("new.date")
    def test_new(self, mock_date):
        mock_date.today.return_value = date(1994, 7, 22)
        try:
            expected_folder = os.path.join("test_base", "src", "1994", "7", "22", "a_test_folder")
            expected_readme = os.path.join(expected_folder, "README.md")
            expected_tags = os.path.join(expected_folder, "tags")

            new.new("a_test_folder")

            self.assertTrue(os.path.exists(expected_folder))
            self.assertTrue(os.path.exists(expected_readme))
            self.assertTrue(os.path.exists(expected_tags))
        finally:
            if os.path.exists("test_base"):
                shutil.rmtree("test_base")
