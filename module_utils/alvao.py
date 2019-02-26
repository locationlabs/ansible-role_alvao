# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Avast Software s.r.o.
# This code is licensed under MIT license (see LICENSE or https://opensource.org/licenses/MIT)

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

AUTH_REQUEST_HEADER = {'Content-Type': 'application/x-www-form-urlencoded'}
OBJECT_HEADER = {'Content-Type': 'application/json'}
AUTH_TOKEN_ENDPOINT = '/oauth2/token'
QUERY_ENDPOINT = '/objects'
OBJECT_ENDPOINT = QUERY_ENDPOINT + '/{}'
OBJECT_UPDATE_ENDPOINT = OBJECT_ENDPOINT + '/properties'


def _request(module, endpoint, method='GET', **kwargs):
    """Send REST API requests to Alvao server.

    Returns requests.Response object
    """
    if not HAS_REQUESTS:
        module.fail_json(
            msg="Requests library is required by this module."
        )

    if module.params.get('auth'):
        auth = module.params.get('auth')
        url = auth['api_url'] + endpoint
        verify = auth['validate_certs']
    else:
        url = module.params.get('api_url') + endpoint
        if url.startswith('https'):
            verify = module.params.get('validate_certs')
            if not verify:
                module.log("Will not validate certs for https endpoint, disabling urllib3 warnings")
                requests.packages.urllib3.disable_warnings()
        else:
            verify = False

    module.log("Endpoint: {}".format(endpoint))

    try:
        response = requests.request(
            method=method,
            url=url,
            verify=verify,
            **kwargs
        )
        module.log("Headers: {}".format(response.request.headers))
        module.log("Status code: {}".format(response.status_code))
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        module.fail_json(
            msg=str(e)
        )


def _auth_header(module):
    """Generate an authentication header from a token."""
    token = module.params.get('auth')['access_token']
    auth_header = {
        'Authorization': 'Bearer {}'.format(token)
    }

    return auth_header


def auth_token(module, auth_data):
    """Request authentication token.

    Returns JSON."""
    auth_token_data = _request(
        module,
        endpoint=AUTH_TOKEN_ENDPOINT,
        headers=AUTH_REQUEST_HEADER,
        data=auth_data
    )

    return auth_token_data.json()


def query(module):
    """Query Alvao for objects matching the given search query.

    Returns JSON."""
    query_data = _request(
        module,
        endpoint=QUERY_ENDPOINT,
        headers=_auth_header(module),
        params=module.params.get('query')
    )

    return query_data.json()


def query_object(module):
    """Query Alvao for a specific object by node ID.

    Returns JSON."""
    object_data = _request(
        module,
        endpoint=OBJECT_ENDPOINT.format(module.params.get('node_id')),
        headers=_auth_header(module)
    )

    # The api docs says I'm supposed to get a {...} but instead we get [{...}] :/
    return object_data.json()[0]


def update(module):
    """Update specific Alvao object.

    Returns requests.Response.status_code."""
    header = _auth_header(module)
    header.update(OBJECT_HEADER)
    update_response = _request(
        module,
        endpoint=OBJECT_UPDATE_ENDPOINT.format(module.params.get('node_id')),
        method='PATCH',
        headers=header,
        json=module.params.get('data')
    )

    return update_response.status_code


def object_properties(data):
    """Transform an Alvao object's properties into a dictionary."""
    properties = {p['name']: p['value'] for p in data['properties']}

    return properties
