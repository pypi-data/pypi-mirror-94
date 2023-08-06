"""Pre-analysis operations such as gathering intel about known modules.

Cache can be generated using `ansible_mkdocs.cache.generate_cache`.
"""
from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path
from typing import List


@dataclass
class AnsibleModule:
    name: str
    collection: str
    requirements: str
    parameters: List[str]  # could be dict or struct


def find_known_modules():
    """Load module informations in cache and extra directories."""
    for module in chain(cached_modules, extra_directories):
        yield module
