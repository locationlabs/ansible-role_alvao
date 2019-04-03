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
module: alvao_create
short_description: "Create a new Alvao object"
author: "David M Noriega (@davidmnoriega)"
description:
    Create a new object in Alvao
requirements:
    - "python >= 2.7"
    - requests
options:
    auth:
        required: True
        type: dict
        description:
            - "Auth data returned by the alvao_auth module"
    template_node_id:
        required: True
        type: int
        description:
            - "Node ID of the template object to create the new object from"
    parent_node_id:
        required: True
        type: int
        description:
            - "Node ID of the object that will be the parent of the new object"
'''

RETURN = r'''
object_data:
    description: Object creation response from Alvao
    returned: success
    type: complex
    contains:
        object_data:
            description: "New object's properties - Truncated list of properties to follow"
            returned: success
            type: complex
            contains:
                class:
                    description: Type of Alvao object
                    type: string
                    returned: success
                name:
                    description: Name of Alvao object
                    type: string
                    returned: success
                path:
                    description: Path of Alvao object
                    type: string
                    returned: success
                properties:
                    description: List of all object's properties
                    type: list
                    returned: success
                nodeId:
                    description: Object's Node ID
                    returned: success
                    type: int
                    sample: 54321
'''

EXAMPLES = r'''
- alvao_create:
    auth: "{{ alvao_auth }}"
    template_node_id: 54321
    parent_node_id: 12345
  register: new_object

- debug:
    var: new_object
'''

from ansible.module_utils.basic import AnsibleModule
import ansible.module_utils.alvao as alvao


def main():
    module = AnsibleModule(
        argument_spec=dict(
            auth=dict(required=True, type=dict, no_log=True),
            template_node_id=dict(required=True, type=int),
            parent_node_id=dict(required=True, type=int)
        ),
        supports_check_mode=True
    )

    if not module.check_mode:
        response = alvao.create(module)
        module.exit_json(
            changed=True,
            message="Alvao object created",
            object_data=response
        )
    else:
        module.exit_json(
            changed=True,
            message="Alvao object created"
        )


if __name__ == "__main__":
    main()
