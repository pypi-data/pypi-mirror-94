# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ansible_mkdocs']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['ansible-mkdocs = ansible_mkdocs.main:make_docs']}

setup_kwargs = {
    'name': 'ansible-mkdocs',
    'version': '0.0.2',
    'description': 'Auto-generate ansible role documentation',
    'long_description': "# ansible-document\n\nAutomatically document ansible roles.\n\n## Concept\n\nGenerate documentation automatically by looking up a role's content.\n\n## Usage\n\n```console\n$ ansible-mkdocs path/to/role\n# ex:\n$ ansible-mkdocs examples/install_gitlab\nname | value | location\n------|------|------\ngitlab_package_script_url | https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | vars/main.yml\ngitlab_interface | {{ ansible_default_ipv4['interface'] }} | defaults/main.yml\ngitlab_addr | {{ hostvars[inventory_hostname]['ansible_' + gitlab_interface]['ipv4']['address']  }} | defaults/main.yml\ngitlab_install | yes | defaults/main.yml\n```\n\n## How does it work?\n\n- Generate a list with modules and their values\n    - Example: copy will be used, register the mode, required, ...\n- Lookup every directory (files, tasks, vars, ...) and fetch information\n    - For every directory, generate the associated template\n- Aggregate every generated templates\n- Add metadata\n    - Has tests\n    - Has molecule\n    - Meta from meta/\n- Output markdown\n",
    'author': 'Theo "Bob" Massard',
    'author_email': 'tbobm@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tbobm/ansible-mkdocs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
