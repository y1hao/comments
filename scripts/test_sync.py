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

    def assertContainsInOrder(self, text: str, *parts: str):
        index = -1
        for word in parts:
            index = text.find(word, index+1)
            if index == -1:
                self.assertNotEqual(-1, index, f"'{word}' is not found in string")

    @patch("paths.BASE_PATH", os.path.join("scripts", "test_files", "sync_test"))
    @patch("sync.PAGE_SIZE", 2)
    def test_sync(self):
        base = os.path.join("scripts", "test_files", "sync_test")
        try:
            # setup:
            # test1: 2021-6-21
            # test2: 2021-6-22, TypeScript
            # test3: 2022-6-21, C#, TypeScript
            # test4: 2022-6-22, draft, Hello

            sync.sync()

            # generate README.md
            with open(os.path.join(base, "README.md"), encoding="utf-8") as readme:
                text = readme.read()
                # sorting order being test3 - test2 - test3
                # page size is 2
                self.assertContainsInOrder(text, "[test3]", "[test2]")

                # draft not shown
                self.assertNotIn("test4", text)

                # not on first page
                self.assertNotIn("test1", text)

            # generate archive.md
            with open(os.path.join(base, "index", "archive.md"), encoding="utf-8") as archive:
                text = archive.read()
                self.assertContainsInOrder(text,
                                           "## 2022",
                                           "[test4]",
                                           "[test3]",
                                           "## 2021",
                                           "[test2]",
                                           "[test1]")

            # generate tags.md
            with open(os.path.join(base, "index", "tags.md"), encoding="utf-8") as tags:
                text = tags.read()
                self.assertContainsInOrder(text,
                                           "## C#",
                                           "[test3]",
                                           "## Hello",
                                           "[test4]",
                                           "## TypeScript",
                                           "[test3]",
                                           "[test2]",
                                           "## draft",
                                           "[test4]")

            # generate pages
            with open(os.path.join(base, "index", "pages", "1.md"), encoding="utf-8") as page:
                text = page.read()
                # sorting order being test3 - test2 - test3
                # page size is 2
                self.assertContainsInOrder(text, "[test3]", "[test2]")

                # draft not shown
                self.assertNotIn("test4", text)

                # not on first page
                self.assertNotIn("test1", text)

            with open(os.path.join(base, "index", "pages", "2.md"), encoding="utf-8") as page:
                text = page.read()
                # sorting order being test3 - test2 - test3
                # page size is 2
                self.assertContainsInOrder(text, "[test1]")

                # draft not shown
                self.assertNotIn("test4", text)

                # not on this page
                self.assertNotIn("test2", text)
                self.assertNotIn("test3", text)
        
        finally:
            if os.path.exists(os.path.join(base, "index")):
                shutil.rmtree(os.path.join(base, "index"))
            if os.path.exists(os.path.join(base, "README.md")):
                os.remove(os.path.join(base, "README.md"))