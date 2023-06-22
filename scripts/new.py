import os
import sys
from datetime import date

import paths
import template


def new(folder_name: str) -> None:
    """Create a new snippet folder with the given folder name"""

    # Create path
    snippet_path = paths.snippet_path(folder_name, date.today())
    if os.path.exists(snippet_path):
        print(f"The folder '{snippet_path}' already exists. Try another name.", file=sys.stderr)
        sys.exit(1)
    os.makedirs(snippet_path, exist_ok=True)

    # Create README.md

    home_link = f"[Home]({paths.rel(paths.base(), snippet_path)}/README.md)"
    readme = (template.load("README.md")
              .replace("{title}", folder_name)
              .replace("{home_link}", home_link))
    with open(os.path.join(snippet_path, "README.md"), "x", encoding="utf-8") as file:
        file.write(readme)

    # Create tags file
    template.copy("tags", os.path.join(snippet_path, "tags"))

    print(f"Snippet folder created: '{snippet_path}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        folder_name = input("Input the snippet folder name: ")
    else:
        folder_name = sys.argv[1]
    new(folder_name)
