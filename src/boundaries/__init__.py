import sys

import parso

__all__ = ["main", "Module"]


def main():
    loader = Loader()
    for arg in sys.argv[1:]:
        module = loader.load(arg)
        print(module.path, module.is_package)
        for x in sorted(module.exports):
            print("   ", x)
        print("    --")
        for x in sorted(module.imports):
            print("   ", x)


class Export:
    def __init__(self, name, is_imported):
        self.name = name
        self.is_imported = is_imported
        self._as_tuple = None

    @property
    def as_tuple(self):
        if self._as_tuple is None:
            self._as_tuple = (self.name, self.is_imported)
        return self._as_tuple

    def __eq__(self, other):
        return type(self) == type(other) and self.as_tuple == other.as_tuple

    def __hash__(self):
        return hash(self.as_tuple)

    def __lt__(self, other):
        return type(self) == type(other) and self.as_tuple < other.as_tuple

    def __repr__(self):
        return repr(self.as_tuple)


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


class Loader:
    def __init__(self, sys_path=None):
        self._cache = {}
        self._sys_path = sys_path

    def load(self, path):
        with open(path) as f:
            code = f.read()

        module = self.parse(code, path)
        # TODO cache module
        return module

    def parse(self, code, path, is_package=None):
        tree = parso.parse(code)
        return Module(path, tree, is_package, self)


class Module:
    def __init__(self, path, tree, is_package, loader):
        self.is_package = is_package
        self.loader = loader
        self.path = path
        self.tree = tree
        self._exports = None
        self._imports = None

    @property
    def exports(self):
        if self._exports is not None:
            return self._exports

        def walk(tree, is_imported):
            if tree.type == "name":
                if tree.is_definition():
                    exports.add(Export(tree.value, is_imported))
            elif tree.type in ("classdef", "funcdef"):
                exports.add(Export(tree.name.value, is_imported))
            elif tree.type in ("import_from", "import_name"):
                for subtree in tree.children:
                    walk(subtree, True)
            elif hasattr(tree, "children"):
                for subtree in tree.children:
                    walk(subtree, is_imported)

        exports = set()
        walk(self.tree, False)
        self._exports = exports

        return exports

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
