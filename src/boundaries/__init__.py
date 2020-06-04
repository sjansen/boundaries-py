import sys

import parso

__all__ = ["main", "Module"]


def main():
    for arg in sys.argv[1:]:
        module = Module.parse(arg)
        print(module.path)
        for x in sorted(module.exports):
            print("   ", x)
        print("    --")
        for x in sorted(module.imports):
            print("   ", x)


class Import:
    def __init__(self, dotted_name, is_inline, is_module):
        self.dotted_name = dotted_name
        self.is_inline = is_inline
        self.is_module = is_module
        self._as_tuple = None

    @property
    def as_tuple(self):
        if self._as_tuple is None:
            self._as_tuple = (self.dotted_name, self.is_inline, self.is_module)
        return self._as_tuple

    def __eq__(self, other):
        return type(self) == type(other) and self.as_tuple == other.as_tuple

    def __hash__(self):
        return hash(self.as_tuple)

    def __lt__(self, other):
        return type(self) == type(other) and self.as_tuple < other.as_tuple

    def __repr__(self):
        return repr(self.as_tuple)


class Module:
    @classmethod
    def parse(cls, path):
        with open(path) as f:
            code = f.read()
        tree = parso.parse(code)
        return cls(path, tree)

    def __init__(self, path, tree):
        self.path = path
        self.tree = tree
        self._exports = None
        self._imports = None

    @property
    def exports(self):
        if self._exports is not None:
            return self._exports

        def walk(tree, is_inline):
            if tree.type in ("classdef", "funcdef"):
                names.add(tree.name.value)
            elif tree.type == "name":
                if tree.is_definition():
                    names.add(tree.value)
            elif hasattr(tree, "children"):
                for subtree in tree.children:
                    walk(subtree, is_inline)

        names = set()
        walk(self.tree, False)
        self._exports = names

        return names

    @property
    def imports(self):
        if self._imports is not None:
            return self._imports

        def walk(tree, is_inline):
            if tree.type == "import_from":
                for path in tree.get_paths():
                    dotted_name = ".".join(name.value for name in path)
                    imports.add(Import(dotted_name, is_inline, False))
            elif tree.type == "import_name":
                for path in tree.get_paths():
                    dotted_name = ".".join(name.value for name in path)
                    imports.add(Import(dotted_name, is_inline, True))
            elif tree.type in ("classdef", "funcdef"):
                for subtree in tree.children:
                    walk(subtree, True)
            elif hasattr(tree, "children"):
                for subtree in tree.children:
                    walk(subtree, is_inline)

        imports = set()
        walk(self.tree, False)
        self._imports = imports

        return imports
