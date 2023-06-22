from typing import Iterable, Tuple, List, Callable

import paths
import template
from snippets import Snippet

SnippetPage = Iterable[Snippet]
SnippetsByYear = Iterable[Tuple[int, Iterable[Snippet]]]
SnippetsByTag = Iterable[Tuple[str, Iterable[Snippet]]]

def gen_page(
        snippets: SnippetPage, 
        total_pages: int,
        current_page: int, 
        current_path: str) -> str:
    """Generate contents on one page"""
    templ = template.load("page.md")
    header = _gen_header(current_path)
    items = "\n".join(_gen_item(snippet, current_path) for snippet in snippets)
    pagination = _gen_pagination(total_pages, current_page, current_path)
    return (templ.replace("{pagination}", pagination)
            .replace("{header}", header)
            .replace("{items}", items))

def gen_archive(snippets_by_year: SnippetsByYear) -> str:
    """Generate the archive index"""
    current_path = paths.index()
    templ = template.load("archive.md")
    header = _gen_header(current_path)
    items: List[str] = []
    for year, snippets in snippets_by_year:
        items.append(f"## {year}")
        for snippet in snippets:
            items.append(_gen_item(snippet, current_path, show_summary=False))
    return (templ.replace("{header}", header)
            .replace("{items_by_year}", "\n".join(items)))

def gen_tags(snippets_by_tag: SnippetsByTag) -> str:
    """Generate the tags index"""
    current_path = paths.index()
    templ = template.load("tags.md")
    header = _gen_header(current_path)
    all_tags = _gen_all_tags(tag for tag, _ in snippets_by_tag)
    items: List[str] = []
    for tag, snippets in snippets_by_tag:
        items.append(f"## {tag}\n")
        for snippet in snippets:
            items.append(_gen_item(snippet, current_path, show_summary=False))
        items.append("")
    return (templ.replace("{header}", header)
            .replace("{all_tags}", all_tags)
            .replace("{items_by_tag}","\n" .join(items)))

def _gen_header(current_path: str) -> str:
    home = f"[Home]({paths.rel(paths.base(), current_path)}/README.md)"
    archive = f"[Archive]({paths.rel(paths.index(), current_path)}/archive.md)"
    tags = f"[Tags]({paths.rel(paths.index(), current_path)}/tags.md)"
    return " | ".join([home, archive, tags])

def _gen_item(
        snippet: Snippet, 
        current_path: str, 
        show_summary: bool = True) -> str:
    link = f"{paths.rel(paths.snippet_path(snippet.path, snippet.created), current_path)}/README.md"
    parts: List[str] = []
    parts.append(f"- __[{snippet.title}]({link})__")
    parts.append(f"  _`{snippet.created}`_")
    parts.append(f"  {_gen_tags(snippet, current_path)}\n")

    if show_summary:
        parts.append(f"  > {snippet.summary}")
    return "\n".join(parts)

def _gen_pagination(
        total_pages: int, 
        current_page: int, 
        current_path: str) -> str:
    make_link: Callable[[str], str] = lambda p: f"{paths.rel(paths.pages(), current_path)}/{p}.md"
    
    links: List[str] = []
    has_newer = current_page != 1
    has_older = current_page != total_pages

    if has_newer:
        links.append(f"[Newer]({make_link(str(current_page - 1))})")
    
    for i in range(1, total_pages + 1):
        if i != current_page:
            links.append(f"[{str(i)}]({make_link(str(i))})")
        else:
            links.append(str(i))

    if has_older:
        links.append(f"[Older]({make_link(str(current_page + 1))})")

    return " | ".join(links)

def _gen_all_tags(tags: Iterable[str]) -> str:
    make_tag: Callable[[str], str] = lambda t: f"[{t}](./tags.md#{t})"
    return "All tags: " + ", ".join(make_tag(tag) for tag in tags)

def _gen_tags(snippet: Snippet, current_path: str) -> str:
    make_tag: Callable[[str], str] = lambda t: f"[{t}]({paths.rel(paths.index(), current_path)}/tags.md#{t})"
    links = [make_tag(t) for t in sorted(snippet.tags)]
    return ", ".join(links)