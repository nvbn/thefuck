#!/usr/bin/env python3
"""
Removes type annotation from source code.
"""

from typed_ast import ast3 as ast
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path
from astunparse import unparse


class TypeEraser(ast.NodeTransformer):
    def visit_arg(self, node):
        node.annotation = None
        return node

    def visit_FunctionDef(self, node):
        node.returns = None
        return self.generic_visit(node)


def get_all_python_files():
    root = Path(__file__).parent.joinpath('thefuck')
    return root.glob('**/*.py')


def remove_annotations(path):
    code = path.open().read()
    tree = ast.parse(code)
    TypeEraser().visit(tree)
    without_annotations = unparse(tree)
    with path.open('w') as f:
        f.write(without_annotations)


def run():
    for path in get_all_python_files():
        remove_annotations(path)


if __name__ == '__main__':
    run()
