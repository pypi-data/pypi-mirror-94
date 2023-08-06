"""Main module.

generate doc:
- Generate list of modules with values
- Lookup directories and fetch information
- Aggregate every generated templates
- Add metadata
- Output markdown

generate cache:
"""
from pathlib import Path
import itertools
import click

from ansible_mkdocs import gather, output, role, setup


@click.command()
@click.argument('path', type=click.Path(exists=True))
def make_docs(path):
    # known_modules = setup.find_known_modules()
    _role = role.Role(Path(path))
    defs = gather.find_variable_definitions(_role.path)
    listed = itertools.chain.from_iterable([gather.inspect_definition(_def) for _def in defs])
    print(output.generate_documentation(listed))
    # role.introspect(verbose=False)
    # component:
    #   component_type: vars
    #   content:
    #     executable_directory:
    #       value: /opt/bin
    #       comment: "Install in default common installation directory."
    #       file: main.yml
    #

    #  role.set_components(role.fetch_components())
    #  Role.render(template=None)
    #
    # https://jinja.palletsprojects.com/en/2.11.x/templates/#macros

    # can lead to:
    #   Playbook(roles)
    #   playbook.render(template=None) (then for component component.render())

    # documentation = """"""  # playbook.render(template=None)
    # print(documentation)


if __name__ == '__main__':
    make_docs()
