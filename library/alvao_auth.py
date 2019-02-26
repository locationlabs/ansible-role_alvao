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
module: alvao_auth
short_description: "Retrieve an auth token"
author: "David M Noriega (@davidmnoriega)"
description:
    Retrieve an auth token from an Alvao server
requirements:
    - "python >= 2.7"
    - requests
options:
    url:
        required: True
        description:
            - "A string containing the base API URL of the Alvao server for retrieving an auth token.
                For example: I(https://alvao.example.com)
                Default value is set by C(ALVAO_URL) environment variable."
    username:
        required: True
        description:
            - "The name of the user, in the form of C(DOMAIN\\\\username)
                Default value is set by C(ALVAO_USERNAME) environment variable."
    password:
        required: True
        description:
            - "The password of the user. Default value is set by C(ALVAO_PASSWORD) environment variable."
    validate_certs:
        required: False
        default: 'yes'
        type: bool
        description:
            - "If using https, validate SSL certificate."
'''

RETURN = r'''
alvao_auth:
    description: Authentication response from Alvao
    returned: success
    type: complex
    contains:
        token:
            description: SSO token used for making requests to Alvao
            returned: success
            type: string
        token_type:
            description: Token type
            returned: success
            type: string
            sample: "bearer"
        expires_in:
            description: Token lifetime
            returned: success
            type: int
            sample: 1799
        validate_certs:
            desciption: If using https, validate SSL certificate
            returned: success
            type: bool
            sample: True
        url:
            desciption: Url used to establish authentication
            returned: success
            type: string
            sample: https://alvao.example.com
'''

EXAMPLES = r'''
- alvao_auth:
    url: "https://alvao.example.com"
    username: "DOMAIN\\username"
    password: "{{ alvao_password }}"

- alvao_facts:
    auth: "{{ alvao_auth }}"
    query: "{{ search_query }}"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
from ansible.module_utils.api import basic_auth_argument_spec
from ansible.module_utils.common.dict_transformations import dict_merge
import ansible.module_utils.alvao as alvao

auth_argument_spec_mod = dict(
    api_username=dict(required=True, fallback=(env_fallback, ['ALVAO_USERNAME'])),
    api_password=dict(required=True, fallback=(env_fallback, ['ALVAO_PASSWORD'])),
    api_url=dict(required=True, fallback=(env_fallback, ['ALVAO_URL'])),
    validate_certs=dict(required=False)
)
auth_argument_spec = dict_merge(basic_auth_argument_spec(), auth_argument_spec_mod)


def main():
    module = AnsibleModule(
        argument_spec=auth_argument_spec,
        supports_check_mode=True
    )

    auth_data = {
        'grant_type': 'password',
        'username': module.params.get('api_username'),
        'password': module.params.get('api_password'),
    }

    auth_token_data = alvao.auth_token(module, auth_data)
    for key in ('validate_certs', 'api_url'):
        auth_token_data[key] = module.params.get(key)

    module.exit_json(
        changed=False,
        ansible_facts=dict(
            alvao_auth=auth_token_data
        )
    )


if __name__ == "__main__":
    main()
