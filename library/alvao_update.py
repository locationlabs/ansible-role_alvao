#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Avast Software s.r.o.
# This code is licensed under MIT license (see LICENSE or https://opensource.org/licenses/MIT)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = r'''
---
module: alvao_update
short_description: "Update Alvao object"
author: "David M Noriega (@davidmnoriega)"
description:
    Update Alvao object data
requirements:
    - "python >= 2.7"
    - requests
options:
    auth:
        required: True
        type: dict
        description:
            - "Auth data returned by the alvao_auth module"
    node_id:
        required: True
        description:
            - "Node ID of the object to update"
    data:
        required: True
        type: dict
        description:
            - "Dictionary of Alvao field keys and values to update the object"
'''

EXAMPLES = r'''
- alvao_update:
    auth: "{{ alvao_auth }}"
    node_id: "{{ node_id }}"
    data: "{{ update_data }}"
  vars:
    update_data:
      "Alvao object field name": "value"
'''

from ansible.module_utils.basic import AnsibleModule
import ansible.module_utils.alvao as alvao


def main():
    module = AnsibleModule(
        argument_spec=dict(
            auth=dict(required=True, type=dict, no_log=True),
            node_id=dict(required=True),
            data=dict(required=True, type=dict)
        ),
        supports_check_mode=True
    )

    diff = {}
    object_data = alvao.query_object(module)
    object_properties = alvao.object_properties(object_data)
    new_object_properties = object_properties.copy()
    new_object_properties.update(module.params.get('data'))

    if object_properties == new_object_properties:
        module.exit_json(changed=False)
    elif module._diff:
        diff = {
            'before': object_properties,
            'after': new_object_properties
        }

    if not module.check_mode:
        response_code = alvao.update(module)
        if response_code != 204:
            module.fail_json(
                msg="Unexpected response code: {}".format(response_code)
            )

    module.exit_json(
        changed=True,
        message="Alvao object updated",
        diff=diff
    )


if __name__ == "__main__":
    main()
