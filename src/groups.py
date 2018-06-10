import requests
from time import sleep
import json


ACCESS_TOKEN = 'df648b36826b60888525e47f2b868a41a2b582f7c7c0e9949e2e335e2195d6031eaca5e8fcb92d4a49d5b'


def get_response_json(method, parameters):
    params = dict(
        v='5.74',
        access_token=ACCESS_TOKEN
    )
    params.update(parameters)

    response = requests.get(
        'https://api.vk.com/method/{}'.format(method),
        params=params
    )
    return response.json()


def get_user_id(domain):
    response = get_response_json(
        'users.get',
        parameters=dict(
            user_ids=domain
        )
    )
    user_id = response['response'][0]['id']
    return user_id


def get_entity_ids(entity, user_id):
    if isinstance(user_id, str):
        user_id = get_user_id(user_id)
    print('Getting {} for user {}'.format(entity, user_id))
    response = get_response_json(
        '{}.get'.format(entity),
        parameters=dict(
            user_id=user_id
        )
    )
    ids = response['response']['items']
    return set(ids)


def get_user_friends(user_id):
    return get_entity_ids('friends', user_id)


def get_user_groups(user_id):
    return get_entity_ids('groups', user_id)


def get_group_data(group_ids):
    response = get_response_json(
        'groups.getById',
        parameters=dict(
            group_ids=get_separated_string_list(group_ids),
            fields='members_count'
        )
    )
    return response['response']


def get_separated_string_list(int_list):
    return ','.join(str(x) for x in int_list)


def get_difference_set(user_group_ids, user_friend_ids):
    friends_groups = set()
    for friend in user_friend_ids:
        friend_groups = get_user_groups(friend)
        friends_groups.update(friend_groups)
        print(len(friends_groups))
        sleep(0.5)

    print(friends_groups)
    print(len(friends_groups))

    diff = user_group_ids.difference(friends_groups)
    return diff


def main():
    user_groups = get_user_groups(1319072)
    print(user_groups)

    user_friends = get_user_friends(1319072)
    print(user_friends)

    diff = get_difference_set(user_groups, user_friends)
    print(diff)

    group_data = get_group_data(diff)

    # response = get_group_data({66705024, 27121793, 77203330, 112643569, 41699702, 135221754})

    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(group_data, f, ensure_ascii=False)


main()
