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
module: alvao_facts
short_description: "Query Alvao"
author: "David M Noriega (@davidmnoriega)"
description: Query Alvao for objects matching the given criteria
requirements:
    - "python >= 2.7"
    - requests
options:
    auth:
        required: True
        type: dict
        description:
            - "Auth data returned by the alvao_auth module"
    query:
        required: True
        type: dict
        description:
            - "Search query"
'''

RETURN = r'''
alvao_facts:
    description: "Dictionary containing reponse from Alvao object API"
    returned: success
    type: complex
    contains:
        count:
            description: Number of results per page
            type: int
            returned: success
        page:
            description: Number of pages
            type: int
            returned: success
        total:
            description: Total number of results
            type: int
            returned: success
        results:
            description: "List of dictionaries describing the Alvao objects
                         matching the search query"
            type: list
            returned: success
'''

EXAMPLES = r'''
- alvao_facts:
    auth: "{{ alvao_auth }}"
    query: "{{ search_query }}"
  vars:
    search_query:
      class: "Computer/server"
'''

from ansible.module_utils.basic import AnsibleModule
import ansible.module_utils.alvao as alvao


def main():
    module = AnsibleModule(
        argument_spec=dict(
            auth=dict(required=True, type=dict, no_log=True),
            query=dict(type=dict)
        ),
        supports_check_mode=True
    )

    module.exit_json(
        changed=False,
        ansible_facts=dict(
            alvao_facts=alvao.query(module)
        )
    )


if __name__ == "__main__":
    main()
