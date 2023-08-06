"""Display the role documentation."""
from textwrap import dedent
from typing import List

from ansible_mkdocs.types import AnsibleVar

HEADER = 'name | value | location'
SEPARATOR = "------|------|------"


def generate_documentation(variables: List[AnsibleVar]) -> str:
    """Display the variables as a markdown array."""
    content = '\n'.join(variable.render() for variable in variables)
    documentation = HEADER + '\n' + SEPARATOR + '\n' + content
    return documentation
