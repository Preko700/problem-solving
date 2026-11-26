"""Shared pytest fixtures."""
import importlib.util
import pathlib

import pytest


@pytest.fixture
def load_solution():
    """Load the ``solution.py`` that sits next to a test file.

    Many problem folders contain a module with the same name, so each one is
    loaded from its path under a unique module name.
    """

    def _load(test_file):
        path = pathlib.Path(test_file).resolve().with_name("solution.py")
        name = f"solution_{path.parent.parent.name}_{path.parent.name}".replace("-", "_")
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    return _load
