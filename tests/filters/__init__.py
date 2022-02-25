import logging
import requests
import json


class MockManager(object):
    """ Mock manager for filter unit testing. """

    def get_child_logger(self, name):
        return logging.getLogger('test').getChild(name)

    # Fetch pokemon data
    master_file = "https://raw.githubusercontent.com/WatWowMap/" \
        "Masterfile-Generator/master/master-latest-everything.json"
    master_file = requests.get(master_file)
    pokemon_data = master_file.json()["pokemon"]
    with open("data/pokemon_data.json", 'w') as f:
        json.dump(pokemon_data, f, indent=2)
        f.close()

    # Create a geofence.txt for unit tests
    f = open("tests/filters/test_geofences.txt", 'w')
    geo_str = """[NewYork]
40.48683230424025,-74.31541096584718
40.9655644121444,-73.92951619045655
40.9053923299183,-73.72489582912843
40.559904930284,-73.60679280178468"""
    f.write(geo_str)
    f.close()


def generic_filter_test(test):
    """Decorator used for creating a generic filter test.

    Requires the argument to be a function that assigns the following
    attributes when called:
    filt = dict used to generate the filter,
    event_key = key for the event values,
    pass_vals = values that create passing events,
    fail_vals = values that create failing events
    """
    test(test)

    def generic_test(self):
        # Create the filter
        filt = self.gen_filter(test.filt)
        # Test passing
        for val in test.pass_vals:
            event = self.gen_event({test.event_key: val})
            self.assertTrue(
                filt.check_event(event),
                "pass_val failed check in {}: \n{} passed {}"
                "".format(test.__name__, event, filt))
        # Test failing
        for val in test.fail_vals:
            event = self.gen_event({test.event_key: val})
            self.assertFalse(
                filt.check_event(event),
                "fail_val  passed check in {}: \n{} passed {}"
                "".format(test.__name__, event, filt))
    return generic_test


def full_filter_test(test):
    """Decorator used for creating a full filter test.

    Requires the argument to be a function that assigns the following
    attributes when called:
    filt = dict used to generate the filter,
    pass_items = array of dicts that should pass,
    fail_items = array of dicts that should fail
    """
    test(test)

    def full_test(self):
        filt = self.gen_filter(test.filt)

        for val in test.pass_items:
            event = self.gen_event(val)
            self.assertTrue(
                filt.check_event(event),
                "pass_val failed check in {}: \n{} passed {}"
                .format(test.__name__, event, filt))

        for val in test.fail_items:
            event = self.gen_event(val)
            self.assertFalse(
                filt.check_event(event),
                "fail_val  passed check in {}: \n{} passed {}"
                "".format(test.__name__, event, filt))

    return full_test
