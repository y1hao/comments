from dataclasses import dataclass
from datetime import date
from typing import FrozenSet, Iterable, Tuple
from glob import glob
import os

import paths

DRAFT_TAG = "draft"

@dataclass(frozen=True)
class Snippet:
    """Represent a code snippet"""
    title: str
    summary: str
    created: date
    tags: FrozenSet[str]
    path: str
    is_draft: bool

def get_all() -> Iterable[Snippet]:
    """Get all snippets in the repository"""
    for snippet_folder_with_date in glob("*/*/*/*", root_dir=paths.src()):
        year, month, day, name = snippet_folder_with_date.split(os.path.sep)
        created = date(int(year), int(month), int(day))

        title, summary = _readme(snippet_folder_with_date)
        if title == "":
            continue

        tags = frozenset(_tags(snippet_folder_with_date))

        yield Snippet(title, summary, created, tags, name, DRAFT_TAG in tags)

def _readme(folder_with_date: str) -> Tuple[str, str]:
    readme = _file_path(folder_with_date, "README.md")
    if not os.path.exists(readme):
        print(f"Skipping {folder_with_date}: README.md not found")
        return ("", "")

    with open(readme, encoding="utf-8") as file:

        # title is the first non-empty line
        lines = [line.strip() 
                 for line in file.readlines() 
                 if line != "" and not line.isspace()]
        if not lines:
            print(f"Skipping {folder_with_date}: no title defined")

        title = lines[0]
        if title.startswith("#"):
            title = title.lstrip("#").strip()

        # summary is the second non-empty line, or empty if there is no content
        # between the title and a "---"
        if len(lines) < 2 or lines[1] == "---":
            return (title, "")

        return (title, lines[1].lstrip(">").strip())

def _tags(folder_with_date: str) -> Iterable[str]:
    tags = _file_path(folder_with_date, "tags")
    if not os.path.exists(tags):
        return []
    with open(tags, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if len(line) > 0 and not line.startswith("#") and not ' ' in line:
                yield line

def _file_path(folder_with_date: str, filename: str) -> str:
    return os.path.join(paths.src(), folder_with_date, filename)