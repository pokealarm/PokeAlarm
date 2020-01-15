# Standard Library Imports
import operator
# 3rd Party Imports
# Local Imports
from . import BaseFilter
from PokeAlarm.Utilities import MonUtils
from PokeAlarm.Utilities.GruntUtils import get_grunt_id


class GruntFilter(BaseFilter):
    """ Filter class for limiting which invasions trigger a notification. """

    def __init__(self, mgr, name, data):
        """ Initializes base parameters for a filter. """
        super(GruntFilter, self).__init__(mgr, 'invasion', name)

        # Grunts
        self.grunt_ids = self.evaluate_attribute(
            event_attribute='type_id', eval_func=operator.contains,
            limit=BaseFilter.parse_as_nested_set(
                get_grunt_id, 'grunt_types', data))

        # Exclude Grunts
        self.exclude_grunt_ids = self.evaluate_attribute(
            event_attribute='type_id',
            eval_func=lambda d, v: not operator.contains(d, v),
            limit=BaseFilter.parse_as_nested_set(
                get_grunt_id, 'grunt_types_exclude', data))

        # Gender
        self.genders = self.evaluate_attribute(  # f.genders contains m.gender
            event_attribute='gender', eval_func=operator.contains,
            limit=BaseFilter.parse_as_set(
                MonUtils.get_gender_sym, 'grunt_genders', data))

        # Distance
        self.min_dist = self.evaluate_attribute(  # f.min_dist <= m.distance
            event_attribute='distance', eval_func=operator.le,
            limit=BaseFilter.parse_as_type(float, 'min_dist', data))
        self.max_dist = self.evaluate_attribute(  # f.max_dist <= m.distance
            event_attribute='distance', eval_func=operator.ge,
            limit=BaseFilter.parse_as_type(float, 'max_dist', data))

        # Time Left
        self.min_time_left = self.evaluate_attribute(
            # f.min_time_left <= r.time_left
            event_attribute='time_left', eval_func=operator.le,
            limit=BaseFilter.parse_as_type(int, 'min_time_left', data))
        self.max_time_left = self.evaluate_attribute(
            # f.max_time_left >= r.time_left
            event_attribute='time_left', eval_func=operator.ge,
            limit=BaseFilter.parse_as_type(int, 'max_time_left', data))

        # Geofences
        self.geofences = BaseFilter.parse_as_list(str, 'geofences', data)

        # Custom DTS
        self.custom_dts = BaseFilter.parse_as_dict(
            str, str, 'custom_dts', data)

        # Missing Info
        self.is_missing_info = BaseFilter.parse_as_type(
            bool, 'is_missing_info', data)

        # Reject leftover parameters
        for key in data:
            raise ValueError("'{}' is not a recognized parameter for"
                             " Invasion filters".format(key))

    def to_dict(self):
        """ Create a dict representation of this Filter. """
        settings = {}

        # Grunts
        if self.grunt_ids is not None:
            settings['grunt_ids'] = self.grunt_ids

        # Cosmetic
        if self.genders is not None:
            settings['genders'] = self.genders

        # Distance
        if self.min_dist is not None:
            settings['min_dist'] = self.min_dist
        if self.max_dist is not None:
            settings['max_dist'] = self.max_dist

        # Geofences
        if self.geofences is not None:
            settings['geofences'] = self.geofences

        # Missing Info
        if self.is_missing_info is not None:
            settings['missing_info'] = self.is_missing_info

        return settings
