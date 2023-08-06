""":doc:`flake8-assert-check <../index>` flake8 plugin to check if pytests ends up with an assert, a pytest.raise or are disabled for this check."""

import ast
import importlib.metadata
import os
from itertools import islice
from typing import Any, Generator, List, Tuple, Type


def _read_version() -> str:
    try:
        return max(
            importlib.metadata.Distribution.discover(name="flake8_assert_check"),
            key=lambda d: d.version.split("."),
        ).version
    except ValueError:
        return "UNKNOWN"


__version__ = _read_version()


NODE_NAME_START_STR = TEST_FILE_START_STR = "test"
MASSAGE = "FCA100 at least one assert is needed."


def is_assert_or_contains_pytest_raises(node: Any) -> bool:
    """Check if node is of type Assert or With containing an attribute 'raises' with value 'pytest'."""
    if not isinstance(node, ast.Assert):
        if isinstance(node, ast.With):
            for item in node.items:
                item_context = item.context_expr
                if (
                    isinstance(item_context, ast.Attribute)
                    and item_context.attr == "raises"
                ):
                    return True
        return False
    return True


class Visitor(ast.NodeVisitor):
    """Visits every function in the given python file."""

    def __init__(self, filename: str) -> None:
        """Init list of issues and persist path to respective python file."""
        self.problems: List[Tuple[int, int]] = []
        self._filename = filename

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        """Visit functions recursively."""
        if node.name.startswith(NODE_NAME_START_STR):
            with open(self._filename) as f:
                line = next(islice(f, node.lineno - 1, node.lineno))  # type: str
            if not line.strip().endswith("# no_assert"):
                if not any(
                    is_assert_or_contains_pytest_raises(body_item)
                    for body_item in node.body
                ):
                    self.problems.append((node.lineno, node.col_offset))
        self.generic_visit(node)


class Plugin:
    """Entry class of the plugin."""

    name = __name__
    version = __version__

    def __init__(self, tree: ast.AST, filename: str) -> None:
        """Init ast node and persist path to respective python file."""
        self._tree = tree
        self._filename = filename

    def run(
        self,
    ) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:  # noqa: TAE002
        """Check pytest files only, indicated by filenames starting with 'test_'."""
        if os.path.basename(self._filename).startswith(TEST_FILE_START_STR):
            visitor = Visitor(self._filename)
            visitor.visit(self._tree)
            for line, col in visitor.problems:
                yield line, col, MASSAGE, type(self)
