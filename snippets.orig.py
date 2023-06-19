#!/usr/bin/env python3

"""
This script keeps the root level README.md file and tags in sync with code snippets.

Run `snippets.py new folder_name` to create a new snippet folder, and then you can 
place the code snippet files inside this folder.

The generated folder also contains a README.md file and a tags file. The README.md 
file can be used to include any comments and discussions about the snippet. It should
start with a h1 level heading (`# ...`), which is treated as the title. The next 
non-empty line before any headings, if any, is treated as the summary.

The tags file contains the tags attached to the snippet. Each line that does not start
with '#' is treated a tag entry.

Each time a new code snippet is added, `snippets.py sync` should be run, which will 
re-generate the root level README.md file to include a new entry for the added snippet.
It also updates the pages and tags to include the new snippet.
"""

import glob
import os
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List, Tuple

PROG_NAME = os.path.basename(__file__)
BASE_PATH = os.path.dirname(__file__)
CODE_DIR = "src"
INDEX_DIR = "index"
PAGES_DIR = "pages"
TAGS_DIR = "tags"
TEMPLATES_DIR = "_templates"
CODE_PATH = os.path.join(BASE_PATH, CODE_DIR)
INDEX_PATH = os.path.join(BASE_PATH, INDEX_DIR)
PAGES_PATH = os.path.join(INDEX_PATH, PAGES_DIR)
TAGS_PATH = os.path.join(INDEX_PATH, TAGS_DIR)
TEMPLATES_PATH = os.path.join(INDEX_PATH, TEMPLATES_DIR)

PAGE_SIZE = 2

USAGE = f"""Usage:

    {PROG_NAME} new <folder_name>
        Create a new snippet folder.

    {PROG_NAME} sync
        Synchronize README.md and tags with current snippets.

    {PROG_NAME} help
        Print this help info.

    {PROG_NAME} doc
        Print more detailed documentation
"""

@dataclass
class Snippet:
    """Represent a code snippet"""
    title: str
    summary: str
    created: datetime
    tags: List[str]
    path: str

def main():
    """Entry point"""
    if len(sys.argv) < 2:
        error("no command is given")

    command, *args = sys.argv[1:]
    if command == "help" or "--help" in args or "-h" in args:
        print(USAGE)
        sys.exit(0)

    match command:
        case "doc":
            print(__doc__)
            sys.exit(0)
        case "new":
            if len(args) != 1:
                error(f"new: wrong number of arguments, expecting 1, got {len(args)}")
            new(args[0])
        case "sync":
            if len(args) != 0:
                error(f"sync: wrong number of arguments, expecting 0, got {len(args)}")
            sync()
        case _ as command:
            error(f"unrecognized command: {command}")

def new(folder_name: str):
    """Create a new snippet folder with the given folder name"""
    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    folder_path = os.path.join(CODE_PATH, str(year), str(month), str(day), folder_name)

    if os.path.exists(folder_path):
        error(f"The folder '{folder_path}' already exists. Try another name.")

    os.makedirs(folder_path, exist_ok=True)

    with open(os.path.join(TEMPLATES_PATH, "README.template.md"), encoding="utf-8") as file:
        readme = file.read()

    readme = readme.replace("{title}", folder_name)

    with open(os.path.join(folder_path, "README.md"), "x", encoding="utf-8") as file:
        file.write(readme)

    shutil.copyfile(os.path.join(TEMPLATES_PATH, "tags"), os.path.join(folder_path, "tags"))

    print(f"Snippet folder created: '{folder_path}'")

def sync():
    """Synchronize the root level README.md file with the contents in src"""
    snippets = [*get_snippets()]
    print(f"{len(snippets)} snippets found")
    snippets.sort(key=lambda snippet: (snippet.created, snippet.title), reverse=True)
    pages = [*get_pages(snippets)]
    generate_pages(pages)
    generate_tags(snippets)
    with open(os.path.join(BASE_PATH, "README.md"), "w", encoding="utf-8") as file:
        file.write(generate_page_content(pages[0], len(pages), 1))

def get_snippets() -> Iterable[Snippet]:
    """Get all snippets in the repository"""
    for snippet_folder in glob.glob("*/*/*/*", root_dir=CODE_PATH):
        title, summary = get_title_and_summary(snippet_folder)
        if title == "":
            continue
        created = get_created_date(snippet_folder)
        tags = sorted(list(set(get_tags(snippet_folder))))
        yield Snippet(title, summary, created, tags, snippet_folder)

def get_created_date(snippet_folder: str) -> datetime:
    """Get the creation date of the snippet"""
    year, month, day, *_ = snippet_folder.split(os.path.sep)
    return datetime(year=int(year), month=int(month), day=int(day))

def get_title_and_summary(snippet_folder: str) -> Tuple[str, str]:
    """Get the title and the summary of the snippet"""
    filename = os.path.join(CODE_PATH, snippet_folder, "README.md")
    if not os.path.exists(filename):
        print(f"Skipping {snippet_folder}: README.md not found")
        return ("", "")
    
    with open(filename, encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines() if line !="" and not line.isspace()]
        if not lines:
            print(f"Skipping {snippet_folder}: no title defined")

        title = lines[0]
        if title.startswith("#"):
            title = title.lstrip("#").strip()

        if len(lines) < 2:
            return (title, "")

        return (title, lines[1])

def get_tags(snippet_folder: str) -> Iterable[str]:
    """Get all tags in the snippet folder"""
    filename = os.path.join(CODE_PATH, snippet_folder, "tags")
    if not os.path.exists(filename):
        return []
    with open(filename, encoding="utf-8") as file:
        for line in file:
            if len(line.strip()) > 0 and not line.strip().startswith("#"):
                yield line.strip()

def generate_pages(pages: List[List[Snippet]]):
    """Generate snippet pages"""
    if os.path.exists(PAGES_PATH):
        shutil.rmtree(PAGES_PATH)
    os.mkdir(PAGES_PATH)
    for i, page in enumerate(pages):
        generate_page(i+1, page, len(pages))

def generate_page(page_num: int, page: List[Snippet], total_pages: int):
    """Generate a page"""
    with open(os.path.join(PAGES_PATH, f"{str(page_num)}.md"), "w", encoding="utf-8") as file:
        file.write(generate_page_content(page, total_pages, page_num, "../.."))

def generate_page_content(page: Iterable[Snippet], num_pages: int, current: int, path_to_root: str = ".") -> str:
    """Generates content of a page"""
    with open(os.path.join(TEMPLATES_PATH, "page.template.md"), encoding="utf-8") as file:
        template = file.read()
    pagination = generate_pagination(num_pages, current, path_to_root)
    template = template.replace("{pagination}", pagination)
    return template.replace("{items}", "\n".join(generate_entry(snippet, path_to_root=path_to_root) for snippet in page))

def generate_entry(snippet: Snippet, path_to_root, show_tags: bool = True) -> str:
    """Generate an entry of snippet"""
    result = [f"- [{snippet.title}]({snippet_url(snippet, path_to_root)})"]
    result.append(f"`{format_date(snippet.created)}`")
    if show_tags and snippet.tags:
        result.append(" | ".join(f"[{tag}]({tag_url(tag, path_to_root)})" for tag in snippet.tags))
    if snippet.summary:
        result.append(f"  > {snippet.summary}")
    result.append("")
    return "\n".join(result)

def generate_pagination(num_pages: int, current: int, path_to_root: str) -> str:
    """Generate the pagination footer"""
    if num_pages < 2:
        return ""
    has_prev = current != 1
    has_next = current != num_pages
    result = []
    if has_prev:
        result.append(f"[Prev]({page_url(current - 1, path_to_root)})")
    for i in range(1, num_pages + 1):
        if i != current:
            result.append(f"[{i}]({page_url(i, path_to_root)})")
        else:
            result.append(str(i))
    if has_next:
        result.append(f"[Next]({page_url(current + 1, path_to_root)})")
    return " | ".join(result)

def page_url(page_num: int, path_to_root: str) -> str:
    """Get the link for the page"""
    return "/".join([path_to_root, INDEX_DIR, PAGES_DIR, f"{str(page_num)}.md"])

def tag_url(tag: str, path_to_root: str) -> str:
    """Get the link for the tag"""
    return "/".join([path_to_root, INDEX_DIR, TAGS_DIR, f"{tag.lower()}.md"])

def snippet_url(snippet: Snippet, path_to_root: str) -> str:
    """Get the link for the snippet"""
    return "/".join([path_to_root, CODE_DIR, snippet.path.replace(os.path.sep, "/"), "README.md"])

def format_date(date: datetime) -> str:
    """Print date in YYYY-MM-DD"""
    return f"{date.year}-{date.month:02}-{date.day:02}"

def get_pages(snippets: List[Snippet]) -> Iterable[List[Snippet]]:
    """Cut snippets into pages of at most PAGE_SIZE"""
    for i in range(0, len(snippets), PAGE_SIZE):
        yield snippets[i:i+PAGE_SIZE]

def generate_tags(snippets: List[Snippet]):
    """Generate tags"""
    all_tags = set()
    for snippet in snippets:
        all_tags.update(tag.lower() for tag in snippet.tags)

    with open(os.path.join(TEMPLATES_PATH, "tag.template.md"), encoding="utf-8") as file:
        template = file.read()

    all_tag_links = " | ".join(f"[{tag}](./{tag}.md)" for tag in sorted(all_tags))
    template = template.replace("{all_tags}", all_tag_links)

    if os.path.exists(TAGS_PATH):
        shutil.rmtree(TAGS_PATH)
    os.mkdir(TAGS_PATH)

    for tag in all_tags:
        with open(os.path.join(TAGS_PATH, f"{tag}.md"), "w", encoding="utf-8") as file:
            tagged_snippets = [snippet for snippet in snippets 
                               if tag in [tag.lower() for tag in snippet.tags]]
            tagged_snippets.sort(key=lambda snippet: snippet.title)
            items = "\n".join(generate_entry(snippet, path_to_root="../..", show_tags=False) for snippet in tagged_snippets)
            content = template.replace("{tag_name}", tag)
            content = content.replace("{items}", items)
            file.write(content)

def error(message: str):
    """Print error and exit with exit code 1"""
    print(f"{sys.argv[0]}: {message}", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()
