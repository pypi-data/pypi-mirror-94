"""Role structure and functions.

Entrypoint for role related operations.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


COMMON_COMPONENTS = {
    'defaults',
    # 'files',
    # 'tasks',
    # 'templates',
    'vars',
}


@dataclass
class Role:
    """Represent an ansible role to document."""
    name: str = field(init=False)
    path: Path

    # extras.component_names = ['assets']
    extras: Dict = None
    components: List = None # List[ansible_mkdocs.component.Component]

    def introspect(self, verbose=False):
        """Analyze self.path directory."""
        self.gather_infos()
        self.find_components(verbose)
        self.generate_metadata()


    def gather_infos(self):
        pass

    def generate_metadata(self):
        pass

    def find_components(self, verbose):
        """Lookup for known component and explicitly defined."""
        defined_components = self.extras.get('components', set())
        targets = {*COMMON_COMPONENTS, *defined_components}
        for target in targets:
            path = Path(target)
            # ansible_mkdocs.component.Component
            component = Component(target)
            self.components.add(component)
