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
module: alvao_delete
short_description: "Delete an Alvao object"
author: "David M Noriega (@davidmnoriega)"
description:
    Delete an object from Alvao
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
        type: int
        description:
            - "Node ID of the object to delete"
'''

EXAMPLES = r'''
- alvao_delete:
    auth: "{{ alvao_auth }}"
    node_id: 54321
'''

from ansible.module_utils.basic import AnsibleModule
import ansible.module_utils.alvao as alvao


def main():
    module = AnsibleModule(
        argument_spec=dict(
            auth=dict(required=True, type=dict, no_log=True),
            node_id=dict(required=True, type=int)
        ),
        supports_check_mode=True
    )

    if not module.check_mode:
        response_code = alvao.delete(module)
        module.exit_json(
            changed=True,
            message="Alvao object created"
        )
        if response_code != 204:
            module.fail_json(
                msg="Unexpected response code: {}".format(response_code)
            )
    else:
        module.exit_json(
            changed=True,
            message="Alvao object created"
        )


if __name__ == "__main__":
    main()
