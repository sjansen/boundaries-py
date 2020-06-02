import sys

import parso


def main():
    for arg in sys.argv[1:]:
        module = parse_module(arg)
        walk(module)


def parse_module(path):
    with open(path) as f:
        code = f.read()
    return parso.parse(code)


def walk(tree):
    if tree.type in ("import_from", "import_name"):
        print(tree)
        for path in tree.get_paths():
            print(".".join(name.value for name in path))
    if hasattr(tree, "children"):
        for subtree in tree.children:
            walk(subtree)
