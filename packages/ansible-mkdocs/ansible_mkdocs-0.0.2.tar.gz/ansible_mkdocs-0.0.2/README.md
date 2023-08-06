# ansible-document

Automatically document ansible roles.

## Concept

Generate documentation automatically by looking up a role's content.

## Usage

```console
$ ansible-mkdocs path/to/role
# ex:
$ ansible-mkdocs examples/install_gitlab
name | value | location
------|------|------
gitlab_package_script_url | https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | vars/main.yml
gitlab_interface | {{ ansible_default_ipv4['interface'] }} | defaults/main.yml
gitlab_addr | {{ hostvars[inventory_hostname]['ansible_' + gitlab_interface]['ipv4']['address']  }} | defaults/main.yml
gitlab_install | yes | defaults/main.yml
```

## How does it work?

- Generate a list with modules and their values
    - Example: copy will be used, register the mode, required, ...
- Lookup every directory (files, tasks, vars, ...) and fetch information
    - For every directory, generate the associated template
- Aggregate every generated templates
- Add metadata
    - Has tests
    - Has molecule
    - Meta from meta/
- Output markdown
