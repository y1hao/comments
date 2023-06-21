import os
from datetime import date
from functools import cache

# Override this for testing
BASE_PATH = None

# Override this for testing
DATE = date.today()

SRC = "src"
INDEX = "index"
PAGES = "pages"
TAGS = "tags"
TEMPLATES = "templates"

@cache
def scripts() -> str:
    """Returns the directory path containing this script"""
    return os.path.dirname(__file__)

@cache
def templates() -> str:
    """Returns the directory for file templates"""
    return os.path.join(scripts(), TEMPLATES)

@cache
def base() -> str:
    """Returns the base path of this repo, or BASE_PATH if it is defined"""
    if BASE_PATH:
        return BASE_PATH
    return os.path.normpath(os.path.join(scripts(), ".."))

@cache
def src() -> str:
    """Returns the path for the src folder"""
    return os.path.join(base(), SRC)

@cache
def index() -> str:
    """Returns the path for the index folder"""
    return os.path.join(base(), INDEX)

@cache
def pages() -> str:
    """Returns the path for the pages folder"""
    return os.path.join(index(), PAGES)

def rel(path: str, start: str) -> str:
    """Return the relative path to be used in markdown files"""
    return os.path.relpath(path, start).replace(os.path.sep, "/")

def snippet_path(folder_name: str) -> str:
    """Returns the absolute path for a snippet given the folder name"""
    y, m, d = DATE.year, DATE.month, DATE.day
    return os.path.join(src(), str(y), str(m), str(d), folder_name)
