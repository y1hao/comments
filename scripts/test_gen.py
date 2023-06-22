import os
from datetime import date
from unittest import TestCase

import gen
import paths
from snippets import Snippet


class TestGen(TestCase):
    def test_gen_page(self):
        snippets = [
                Snippet("Snippet 1", "Summary 1", date(1994, 7, 22), frozenset(["Hello"]), "s1", False),
                Snippet("Snippet 2", "Summary 2", date(1994, 7, 27), frozenset(["Hello"]), "s2", False)
            ]
        
        page = gen.gen_page(snippets, 2, 1, paths.base())

        with open(os.path.join(os.path.dirname(__file__), "test_files", "gen_test", "page.md"), encoding="utf-8") as file:
            expected = file.read().strip()
            got = page.strip()
            self.assertEqual(got, expected)

    def test_gen_archive(self):
        snippets = [
            (2021, [
                Snippet("Snippet 1", "Summary 1", date(2021, 7, 22), frozenset(["Hello"]), "s1", False),
                Snippet("Snippet 2", "Summary 2", date(2021, 7, 27), frozenset(["Hello"]), "s2", True)
            ]),
            (2022, [
                Snippet("Snippet 3", "Summary 3", date(2022, 7, 22), frozenset(["Hello"]), "s3", False),
                Snippet("Snippet 4", "Summary 4", date(2022, 7, 27), frozenset(["Hello"]), "s4", True)
            ])]
        
        with open(os.path.join(os.path.dirname(__file__), "test_files", "gen_test", "archive.md"), encoding="utf-8") as file:
            expected = file.read().strip()
            got = gen.gen_archive(snippets).strip()
            self.assertEqual(got, expected)

    def test_gen_tag(self):
        snippets = [
            ("hello", [
                Snippet("Snippet 1", "Summary 1", date(2021, 7, 22), frozenset(["hello"]), "s1", False),
                Snippet("Snippet 2", "Summary 2", date(2021, 7, 27), frozenset(["hello"]), "s2", True)
            ]),
            ("world", [
                Snippet("Snippet 3", "Summary 3", date(2022, 7, 22), frozenset(["world"]), "s3", False),
                Snippet("Snippet 4", "Summary 4", date(2022, 7, 27), frozenset(["world"]), "s4", True)
            ])]
        
        with open(os.path.join(os.path.dirname(__file__), "test_files", "gen_test", "tags.md"), encoding="utf-8") as file:
            expected = file.read().strip()
            got = gen.gen_tags(snippets).strip()
            self.assertEqual(got, expected)