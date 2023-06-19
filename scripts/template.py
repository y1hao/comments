import os
import shutil

import paths


def load(template_name: str) -> str:
    """Read all text in a template file"""
    with open(_path(template_name), encoding="utf-8") as template:
        return template.read()

def copy(template_name: str, dst: str):
    """Copy a template file to the dst location"""
    shutil.copy(_path(template_name), dst)

def _path(template_name: str) -> str:
    return os.path.join(paths.templates(), template_name)
