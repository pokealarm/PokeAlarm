import logging
import traceback

from BaseEvent import BaseEvent  # noqa F401
from MonEvent import MonEvent
from StopEvent import StopEvent
from GymEvent import GymEvent
from EggEvent import EggEvent
from RaidEvent import RaidEvent

log = logging.getLogger('Events')


def event_factory(self, data):
    """ Creates and returns the appropriate Event from the given data. """
    try:
        kind = data['type']
        message = data['message']
        if kind == 'pokemon':
            return MonEvent(message)
        elif kind == 'pokestop':
            return StopEvent(message)
        elif kind == 'gym' or kind == 'gym_details':
            return GymEvent(message)
        elif kind == 'raid' and message.get('pkmn_id', 0) == 0:
            return EggEvent(message)
        elif kind == 'raid' and message.get('pkmn_id', 0) != 0:
            return RaidEvent(message)
        elif kind in ['captcha', 'scheduler']:
            log.debug(
                "{} data ignored - unsupported webhook type.".format(kind))
        else:
            raise ValueError("Webhook kind was not an expected value.")
    except Exception as e:
        log.error("Encountered error while converting webhook data"
                  + "({}: {})".format(type(e).__name__, e))
        log.debug("Stack trace: \n {}".format(traceback.format_exec()))
