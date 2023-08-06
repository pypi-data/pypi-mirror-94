"""Gather informations about the target."""
import itertools
import pathlib

from typing import Any, Dict, List

import yaml

from ansible_mkdocs.types import AnsibleVar


def find_variable_definitions(path: pathlib.Path) -> List[pathlib.Path]:
    """Look-up `path` for variable definition.

    `path` must represent a role's top level directory.

    >>> path = pathlib.Path(".")
    >>> print(path.absolute())
    ... PosixPath('.../my-role')
    """
    # search for .yml and .yaml files
    definitions = itertools.chain(path.glob('**/*.yml'), path.glob('**/*.yaml'))
    allowed = ['vars', 'defaults']
    inspectable = [
        definition for definition in definitions
        if any(
            definition.parent.as_posix().endswith(allow)
            for allow in allowed
        )
    ]
    return inspectable


def inspect_definition(path: pathlib.Path) -> List[AnsibleVar]:
    """Fetch the variable definitions from `path`."""
    defined = yaml.safe_load(path.read_bytes())  # type: Dict[str, Any]
    ansible_vars = [
        AnsibleVar(name, value, path)
        for name, value in defined.items()
    ]
    return ansible_vars
