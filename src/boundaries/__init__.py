import sys

import parso


def main():
    for arg in sys.argv[1:]:
        module = Module.parse(arg)
        print(module.path)
        for n in sorted(module.dotted_names):
            print('   ', n)


class Module:
    @classmethod
    def parse(cls, path):
        with open(path) as f:
            code = f.read()
        tree = parso.parse(code)
        return cls(path, tree)

    def __init__(self, path, tree):
        def walk(tree):
            if tree.type == "import_from":
                for path in tree.get_paths():
                    dotted_names.add(".".join(name.value for name in path))
            elif tree.type == "import_name":
                for path in tree.get_paths():
                    dotted_names.add(".".join(name.value for name in path))

            if hasattr(tree, "children"):
                for subtree in tree.children:
                    walk(subtree)

        dotted_names = set()
        walk(tree)

        self.dotted_names = dotted_names
        self.path = path
        self.tree = tree
