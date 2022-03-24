from copy import deepcopy
from dataclasses import dataclass, field, asdict
from inspect import getmembers, isfunction

from arc.tables import table
from shared.settings import logger


@dataclass
class UserModel:
    id: int
    name: str
    password: str


@dataclass
class CatModel:
    id: int
    name: str
    location: str = None


@dataclass
class CatModel(object):
    # Non-default-able Fields
    # user: UserModel
    # Fields with Default Values
    name: str = None
    max_jump_height: float = float(0)
    experience_points: float = None
    favorite_alleys: list = field(default_factory=lambda: [])
    @property
    def fur_color(self):
        fields = f'{self.name}_{self.max_jump_height}_{self.experience_points}'
        # base16fields = int(fields, 16)
        color = str(hash(fields))[1:7]
        return color
    def json(self):
        return model_to_json(self)


cat = CatModel(
    name='Prissy',
    max_jump_height=10,
    experience_points=0,
    favorite_alleys=['Bowling', 'Tornado']
)


def isprop(v):
    return isinstance(v, property)


def model_to_json(model):
    # Read the model as a dictionary
    data = asdict(model)
    # Find all properties so that they can be included in the response
    for name, value in getmembers(model.__class__, isprop):
        # update the dateset
        data.update({name: getattr(model, name)})
    return data


class TestDriver(object):
    """
    A loose implementation of the command chain and specification patterns (following the
    Open-Closed principle) applying the rules and return the updated model for the next rule.
    """
    @staticmethod
    def run(model: CatModel, post_sap_call: False):
        # clone the original model so we don't mess it up
        model = deepcopy(model)

        # iterate all the "specifications" in our "chain"
        for name, func in getmembers(TestDriver, isfunction):
            if name.endswith('_rule'):
                model = func(model, post_sap_call)
            elif name != 'run':
                raise Exception('Remember to name your rule functions ending in _rule ;)')

        return model

    @staticmethod
    def _test_1_rule(model: CatModel):
        if model:
            model.data_2 = 'filled_in'
        return model


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
