import importlib
import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

import paths


class TestGen(TestCase):
    def setUp(self):
        # Force the paths module to reload to get the patches
        # otherwise the patches take no effect because methods in paths are cahced
        importlib.reload(paths)

    @patch("paths.BASE_PATH", "base")
    def test_gen_page(self: TestCase):
        pass

    @patch("paths.BASE_PATH", "base")
    def test_gen_tag(self: TestCase):
        pass