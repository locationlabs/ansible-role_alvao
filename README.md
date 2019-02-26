# alvao

This role has the following modules for interacting with an Alvao inventory server

* `alvao_auth` - Obtain an auth token
* `alvao_facts` - Search Alvao for objects matching a given search query
* `alvao_update` - Update a single Alvao object

See the module documentation for more information: `ansible-doc <module_name>`

## Requirements

* requests

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
