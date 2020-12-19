#!/usr/bin/env python3
"Build a reStructuredText document from the exmaples"

import os
import sys


tutorial = """Tutorial
========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

The tutorial assumes that the example snippets are saved as ``main.py``.

"""

def main():
    print(tutorial)
    _build_examples(os.path.dirname(__file__))


def _build_examples(examples_dir):
    for root, _dirs, files in os.walk(examples_dir):
        if "main.py" not in files:
            continue

        _print_section_title(os.path.join(root, "main.py"))

        for file_name in files:
            _print_include(_get_relpath(examples_dir, root, file_name))


def _get_relpath(examples_dir, root, file_name):
    abspath = os.path.join(root, file_name)
    relpath = os.path.relpath(abspath, examples_dir)
    return relpath


def _print_section_title(file_name):
    with open(file_name) as fp:
        line = fp.readline()

    print()
    title = line.strip().strip('"')
    print(title)
    print("-" * len(title))
    print()


def _print_include(file_name):
    print()
    print(f".. literalinclude:: /examples/{file_name}")

    if file_name.endswith(".py"):
        print("  :language: python")


if __name__ == "__main__":
    main()
