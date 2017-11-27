# Standard Library Imports
import operator
# 3rd Party Imports
# Local Imports
from . import Filter
from PokeAlarm.Utilities import Monster as MonUtils


class Monster(Filter):
    """ Filter class for limiting which events trigger a notification. """

    def __init__(self, name, data):
        """ Initializes base parameters for a filter. """
        super(Monster, self).__init__(name)

        # Monster ID - m.monster_id in f.monster_ids
        self.monster_ids = self.evaluate_attribute(  #
            event_attribute='monster_id', eval_func=operator.contains,
            limit=Filter.parse_as_set(
                MonUtils.get_monster_id, 'monsters', data))

        # Time Left - m.time_left >= f.time_left
        self.time_left = self.evaluate_attribute(
            event_attribute='time_left', eval_func=operator.ge,
            limit=Filter.parse_as_type(int, 'time_left', data))

        # Distance
        self.min_dist = self.evaluate_attribute(  # m.distance >= f.min_dist
            event_attribute='distance', eval_func=operator.ge,
            limit=Filter.parse_as_type(int, 'min_dist', data))
        self.max_dist = self.evaluate_attribute(  # m.distance <= f.max_dist
            event_attribute='distance', eval_func=operator.le,
            limit=Filter.parse_as_type(int, 'min_dist', data))

        # Encounter Stats
        # Level
        self.min_lvl = self.evaluate_attribute(  # m.mon_lvl >= f.min_lvl
            event_attribute='mon_lvl', eval_func=operator.ge,
            limit=Filter.parse_as_type(int, 'min_lvl', data))
        self.max_lvl = self.evaluate_attribute(  # m.mon_lvl <= f.max_lvl
            event_attribute='mon_lvl', eval_func=operator.le,
            limit=Filter.parse_as_type(int, 'max_lvl', data))
        # Attack IV
        self.min_atk = self.evaluate_attribute(  # m.atk_iv >= f.min_atk
            event_attribute='atk_iv', eval_func=operator.ge,
            limit=Filter.parse_as_type(int, 'min_atk', data))
        self.max_atk = self.evaluate_attribute(  # m.atk_iv <= f.max_atk
            event_attribute='atk_iv', eval_func=operator.le,
            limit=Filter.parse_as_type(int, 'max_atk', data))
        # Defense IV
        self.min_def = self.evaluate_attribute(  # m.def_iv >= f.min_def
            event_attribute='def_iv', eval_func=operator.ge,
            limit=Filter.parse_as_type(int, 'min_def', data))
        self.max_def = self.evaluate_attribute(  # m.def_iv <= f.max_def
            event_attribute='def_iv', eval_func=operator.le,
            limit=Filter.parse_as_type(int, 'max_def', data))
        # Stamina IV
        self.min_sta = self.evaluate_attribute(  # m.sta_iv >= f.min_sta
            event_attribute='sta_iv', eval_func=operator.ge,
            limit=Filter.parse_as_type(int, 'min_sta', data))
        self.max_sta = self.evaluate_attribute(  # m.sta_iv <= f.max_sta
            event_attribute='sta_iv', eval_func=operator.le,
            limit=Filter.parse_as_type(int, 'max_sta', data))
        # Percent IV
        self.min_iv = self.evaluate_attribute(  # m.iv >= f.min_iv
            event_attribute='iv', eval_func=operator.ge,
            limit=Filter.parse_as_type(float, 'min_iv', data))
        self.max_iv = self.evaluate_attribute(  # m.iv <= f.max_iv
            event_attribute='iv', eval_func=operator.le,
            limit=Filter.parse_as_type(float, 'max_iv', data))
        # Form
        self.forms = self.evaluate_attribute(  # m.form_id in f.forms
            event_attribute='form_id', eval_func=operator.contains,
            limit=Filter.parse_as_set(int, 'form_ids', data))  # TODO: names

        # Quick Move
        self.quick_moves = self.evaluate_attribute(  # m.q_m in f.q_ms
            event_attribute='quick_move_id', eval_func=operator.contains,
            limit=Filter.parse_as_set(
                MonUtils.get_move_id, 'quick_moves', data))
        # Charge Move
        self.charge_moves = self.evaluate_attribute(  # m.c_m in f.c_ms
            event_attribute='charge_move_id', eval_func=operator.contains,
            limit=Filter.parse_as_set(
                MonUtils.get_move_id, 'charge_moves', data))

        # Cosmetic
        # Gender
        self.genders = self.evaluate_attribute(  # m.gender in f.genders
            event_attribute='gender', eval_func=operator.contains,
            limit=Filter.parse_as_set(
                MonUtils.get_gender_sym, 'genders', data))
        # Height
        self.min_height = self.evaluate_attribute(  # m.height >= f.min_height
            event_attribute='height', eval_func=operator.ge,
            limit=Filter.parse_as_type(float, 'min_height', data))
        self.max_height = self.evaluate_attribute(  # m.height <= f.max_height
            event_attribute='height', eval_func=operator.le,
            limit=Filter.parse_as_type(float, 'max_height', data))
        # Weight
        self.min_weight = self.evaluate_attribute(  # m.weight >= f.min_weight
            event_attribute='weight', eval_func=operator.ge,
            limit=Filter.parse_as_type(float, 'min_weight', data))
        self.max_weight = self.evaluate_attribute(  # m.weight <= f.max_weight
            event_attribute='weight', eval_func=operator.le,
            limit=Filter.parse_as_type(float, 'max_weight', data))
        # Size
        self.sizes = self.evaluate_attribute(  # m.size in f.sizes
            event_attribute='size', eval_func=operator.contains,
            limit=Filter.parse_as_type(
                MonUtils.validate_pokemon_size, 'sizes', data))

        # Missing Info
        self.missing_info = Filter.parse_as_type(bool, 'missing_info', data)

        # Reject leftover parameters
        for key in data:
            raise ValueError("'{}' is not a recognized parameter for"
                             " Monster filters".format(key))

    def to_dict(self):
        """ Create a dict representation of this Filter. """
        settings = {}
        # Monster ID
        if self.monster_ids is not None:
            settings['monster_ids'] = self.monster_ids

        # Time Left
        if self.time_left is not None:
            settings['time_left'] = self.time_left

        # Distance
        if self.min_dist is not None:
            settings['min_dist'] = self.min_dist
        if self.max_dist is not None:
            settings['max_dist'] = self.max_dist

        # Level
        if self.min_lvl is not None:
            settings['min_lvl'] = self.min_lvl
        if self.max_lvl is not None:
            settings['max_lvl'] = self.max_lvl
        # Attack IV
        if self.min_atk is not None:
            settings['min_atk'] = self.min_atk
        if self.max_atk is not None:
            settings['max_atk'] = self.max_atk
        # Defense IV
        if self.min_def is not None:
            settings['min_def'] = self.min_def
        if self.max_def is not None:
            settings['max_def'] = self.max_def
        # Stamina IV
        if self.min_atk is not None:
            settings['min_atk'] = self.min_atk
        if self.min_sta is not None:
            settings['min_sta'] = self.min_sta
        # Percent IV
        if self.min_iv is not None:
            settings['min_iv'] = self.min_iv
        if self.max_iv is not None:
            settings['max_iv'] = self.max_iv
        # Form
        if self.forms is not None:
            settings['forms'] = self.forms

        # Quick Move
        if self.quick_moves is not None:
            settings['quick_moves'] = self.quick_moves
        # Charge Move
        if self.charge_moves is not None:
            settings['charge_moves'] = self.charge_moves

        # Cosmetic
        if self.genders is not None:
            settings['genders'] = self.genders
        # Height
        if self.min_height is not None:
            settings['min_height'] = self.min_height
        if self.max_height is not None:
            settings['max_height'] = self.max_height
        # Weight
        if self.min_weight is not None:
            settings['min_weight'] = self.min_weight
        if self.max_weight is not None:
            settings['max_weight'] = self.max_weight
        # Size
        if self.sizes is not None:
            settings['sizes'] = self.sizes

        # Missing Info
        if self.missing_info is not None:
            settings['missing_info'] = self.missing_info

        return settings