"""Common API-types for ansible_mkdocs."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class AnsibleVar:
    """Ansible variable representation."""
    name: str
    value: Any
    # TODO: Add default
    location: Path

    def render(self) -> str:
        """Render the variable to text."""
        quick_path = f"{self.location.parent.name}/{self.location.name}"
        # NOTE: format self.value based on type
        return (
            f"{self.name} | {self.value} | {quick_path}"
        )
