
from arc.tables import table
from shared.settings import logger


def check_user_cat(user_id=None, cat_id=None):
    # assert user_id and cat_id
    # users_data = table('user')
    # cats_data = table('cats')
    #
    # logger.debug(users_data)
    # logger.debug(cats_data)
    #
    # users = data_tables.user.scan({})
    # cats = data_tables.cats.scan({})

    data_dict = {
        'data_point_1': 'Testing 123',
        'data_point_2': 'Testing 456',
        'data_point_3': 'Testing 789',
        # 'title': "We don't want to overwrite this key because it is a translation"
    }

    return data_dict
