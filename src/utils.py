import requests


def get_response_json(token, method, parameters):
    """
    Utility method to get response from VK API
    :param token: VK access token
    :param method: API method to be called
    :param parameters: a dictionary of parameters for the method
    :return: response json
    """
    params = dict(
        v='5.78',
        access_token=token
    )
    params.update(parameters)

    response = requests.get(
        'https://api.vk.com/method/{}'.format(method),
        params=params
    )
    return response.json()


def get_user_id(token, domain):
    """
    Get user id by his short name
    :param token: VK access token
    :param domain: user's short name in VK API terms
    :return: user id
    """
    response = get_response_json(
        token,
        'users.get',
        parameters=dict(
            user_ids=domain
        )
    )
    if 'error' in response:
        raise ValueError('Could not get id for user {}: {}'.format(domain, response['error']['error_msg']))

    user_id = response['response'][0]['id']
    return user_id


def get_entity_ids(token, entity, user_id):
    """
    Utility method to get a set of ids of a given type
    :param token: VK access token
    :param entity: group, friends, etc
    :param user_id: id of the user
    :return: a set of ids of the given entity
    """
    print('Getting {} for user {}'.format(entity, user_id))
    response = get_response_json(
        token,
        '{}.get'.format(entity),
        parameters=dict(
            user_id=user_id
        )
    )
    if 'error' in response:
        print('Could not get {} for user {}: {}'.format(entity, user_id, response['error']['error_msg']))
        return set()

    ids = response['response']['items']
    return set(ids)


def get_group_data(token, group_ids):
    """
    Get information about a given set of groups, including member count
    :param token: VK access token
    :param group_ids: a set of groups
    :return: json containing data about the groups
    """
    response = get_response_json(
        token,
        'groups.getById',
        parameters=dict(
            group_ids=get_separated_string_list(group_ids),
            fields='members_count'
        )
    )
    return response['response']


def get_separated_string_list(int_list):
    """
    Utility method to transform array into a string separated by commas
    :param int_list: a list of integers to be transformed
    :return: a string containing integers separated by commas
    """
    return ','.join(str(x) for x in int_list)
