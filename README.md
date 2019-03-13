# alvao

This role has the following modules for interacting with an Alvao inventory server

* `alvao_auth` - Obtain an auth token
* `alvao_facts` - Search Alvao for objects matching a given search query
* `alvao_update` - Update a single Alvao object

See the module documentation for more information: `ansible-doc -M <path/to/role/library> <module_name>`

## Requirements

* requests

## Setup

This role does not have any tasks, but for ansible to find the modules without modifying
`ansible.cfg`, import the role in your playbook:

```yaml
---
  - hosts: all
    tasks:
      - name: Import alvao role
        import_role:
          name: alvao

      - name: Fetch alvao auth token
        alvao_auth:
```

Otherwise configure `library` and `module_utils` in your `ansible.cfg`.

## Filters

* `alvao_object_props` - Will return an object's properties as a simple dictionary

Example:

```yaml
- debug:
    msg: "{{ item|alvao_object_props }}"
  with_items: "{{ alvao_facts['results'] }}"
  loop_control:
    label: "{{ item.name }}"
```
