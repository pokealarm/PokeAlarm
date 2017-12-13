# Standard Library Imports
import operator
# 3rd Party Imports
# Local Imports
from . import BaseFilter


class StopFilter(BaseFilter):
    """ Filter class for limiting which stops trigger a notification. """

    def __init__(self, name, data):
        """ Initializes base parameters for a filter. """
        super(StopFilter, self).__init__(name)

        # Distance
        self.min_dist = self.evaluate_attribute(  # f.min_dist <= m.distance
            event_attribute='distance', eval_func=operator.le,
            limit=BaseFilter.parse_as_type(int, 'min_dist', data))
        self.max_dist = self.evaluate_attribute(  # f.max_dist <= m.distance
            event_attribute='distance', eval_func=operator.ge,
            limit=BaseFilter.parse_as_type(int, 'max_dist', data))

        # Missing Info
        self.missing_info = BaseFilter.parse_as_type(
            bool, 'missing_info', data)

        # Reject leftover parameters
        for key in data:
            raise ValueError("'{}' is not a recognized parameter for"
                             " Stop filters".format(key))

    def to_dict(self):
        """ Create a dict representation of this Filter. """
        settings = {}

        # Distance
        if self.min_dist is not None:
            settings['min_dist'] = self.min_dist
        if self.max_dist is not None:
            settings['max_dist'] = self.max_dist

        # Missing Info
        if self.missing_info is not None:
            settings['missing_info'] = self.missing_info

        return settings
