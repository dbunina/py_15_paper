from time import sleep
import os
import json

import utils

# Access token is retrieved in auth.py
ACCESS_TOKEN = 'ed2d9ea1771d166c56bdcb21f3eec18fdefcbc90ad81bd2204216312251f8dd2a615aef0cedaae51a181f'


def get_user_friends(user_id):
    return utils.get_entity_ids(ACCESS_TOKEN, 'friends', user_id)


def get_user_groups(user_id):
    return utils.get_entity_ids(ACCESS_TOKEN, 'groups', user_id)


def get_difference_set(user_group_ids, user_friend_ids):
    friends_groups = set()
    for friend in user_friend_ids:
        friend_groups = get_user_groups(friend)
        friends_groups.update(friend_groups)
        print('Groups subtotal: {}'.format(len(friends_groups)))
        sleep(0.5)  # can't send requests to VK too often
    return user_group_ids.difference(friends_groups)


def get_individual_groups(user_id):
    """
    Get groups for user which none of his friends belongs to
    :param user_id: VK user (id or nickname)
    :return: individual groups data in json format
    """
    if not user_id:
        print('User id should not be empty!')
        return

    if isinstance(user_id, str):
        try:
            user_id = utils.get_user_id(ACCESS_TOKEN, user_id)
        except ValueError:
            print('No user found by username \'{}\', please try again'.format(user_id))
            return

    user_groups = get_user_groups(user_id)
    user_friends = get_user_friends(user_id)

    diff = get_difference_set(user_groups, user_friends)

    return utils.get_group_data(ACCESS_TOKEN, diff) if diff else None


def write_to_file(data):
    output_dir = os.path.join(os.getcwd(), '..', 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, 'groups.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def main():
    user_id = input('Please enter VK user (either id or nickname):').strip()
    group_data = get_individual_groups(user_id)
    write_to_file(group_data)


main()
