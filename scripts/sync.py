import os
from functools import reduce
from itertools import groupby
from operator import itemgetter
from typing import Iterable, List
import shutil

import gen
import paths
import snippets
from gen import SnippetsByTag, SnippetsByYear, SnippetPage
from snippets import Snippet

PAGE_SIZE = 10

def sync() -> None:
    """Synchronize the indexes"""
    all_snippets = sorted(snippets.get_all(), key=lambda s: s.created, reverse=True)

    by_year = sorted(((year, snippets) 
                      for year, snippets in _by_year(all_snippets)),
                      key=itemgetter(0), reverse=True)
    
    by_tag = sorted(((tag, snippets)
                     for tag, snippets in _by_tag(all_snippets)),
                     key=itemgetter(0))
    
    by_page = list(page for page in 
                   _by_page([snippet for snippet in all_snippets 
                             if not snippet.is_draft]))

    _gen_home(by_page[0], len(by_page))
    _gen_pages(by_page)
    _gen_archive(by_year)
    _gen_tags(by_tag)

def _gen_home(snippets: SnippetPage, total_pages: int) -> None:
    current_path = paths.base()
    with open(os.path.join(current_path, "README.md"), "w", encoding="utf-8") as home:
        home.write(gen.gen_page(snippets, total_pages, 1, current_path))

def _gen_pages(snippets: List[SnippetPage]) -> None:
    current_path = paths.pages()

    if os.path.exists(current_path):
        shutil.rmtree(current_path)
    os.makedirs(current_path)

    for i, page in enumerate(snippets):
        with open(os.path.join(current_path, f"{i+1}.md"), "w", encoding="utf-8") as file:
            file.write(gen.gen_page(page, len(snippets), i+1, current_path))

def _gen_archive(snippets_by_year: SnippetsByYear) -> None:
    with open(os.path.join(paths.index(), "archive.md"), "w", encoding="utf-8") as archive:
        archive.write(gen.gen_archive(snippets_by_year))

def _gen_tags(snippets_by_tag: SnippetsByTag) -> None:
    with open(os.path.join(paths.index(), "tags.md"), "w", encoding="utf-8") as tags:
        tags.write(gen.gen_tags(snippets_by_tag))

def _by_year(snippets: SnippetPage) -> SnippetsByYear:
    for year, group in groupby(snippets, key=lambda s: s.created.year):
        yield year, list(group)

def _by_tag(snippets: SnippetPage) -> SnippetsByTag:
    all_tags = reduce(lambda ts, s: ts.union(s.tags), snippets, set())
    for tag in all_tags:
        snippets_with_tag = (snippet for snippet in snippets 
                             if tag in snippet.tags)
        yield tag, snippets_with_tag

def _by_page(snippets: List[Snippet]) -> Iterable[SnippetPage]:
    for i in range(0, len(snippets), PAGE_SIZE):
        yield snippets[i:i+PAGE_SIZE]

if __name__ == "__main__":
    sync()