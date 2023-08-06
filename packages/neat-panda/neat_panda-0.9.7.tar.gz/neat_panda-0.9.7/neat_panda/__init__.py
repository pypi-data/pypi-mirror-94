# -*- coding: utf-8 -*-

"""Top-level package for Neat Panda."""

__author__ = """Henric Sundberg"""
__email__ = "henric.sundberg@gmail.com"
__version__ = "0.9.7"

from ._tidy import spread, gather, flatten_pivot

# from ._caretaker import clean_column_names, _clean_column_names
from ._caretaker import clean_column_names, CleanColumnNames, clean_strings

from ._set_operations import (
    difference,
    intersection,
    symmetric_difference,
    union,
    SetOperations,
)

from ._helpers import _get_version_from_toml
