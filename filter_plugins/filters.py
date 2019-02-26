# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Avast Software s.r.o.
# This code is licensed under MIT license (see LICENSE or https://opensource.org/licenses/MIT)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


# Custom plugins cannot load from custom module_utils, yet...
# See https://github.com/ansible/ansible/issues/28770
def object_properties(data):
    """Transform an Alvao object's properties into a dictionary."""
    properties = {p['name']: p['value'] for p in data['properties']}

    return properties


def alvao_object_props(data):
    if 'properties' not in data:
        raise AnsibleFilterError('alvao_object_props requires a single alvao_facts result')

    return object_properties(data)


class FilterModule(object):
    def filters(self):
        return {
            'alvao_object_props': alvao_object_props
        }
