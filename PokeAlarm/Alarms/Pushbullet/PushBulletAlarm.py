# Standard Library Imports
import requests
import json
# 3rd Party Imports

# Local Imports
from PokeAlarm.Alarms import Alarm
from PokeAlarm.Utils import parse_boolean, require_and_remove_key, \
    reject_leftover_parameters

try_sending = Alarm.try_sending
replace = Alarm.replace


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ATTENTION! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#             ONLY EDIT THIS FILE IF YOU KNOW WHAT YOU ARE DOING!
# You DO NOT NEED to edit this file to customize messages! Please ONLY EDIT the
#     the 'alarms.json'. Failing to do so can cause other feature to break!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ATTENTION! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class PushbulletAlarm(Alarm):
    _defaults = {
        'monsters': {
            'title': "A wild <mon_name> has appeared!",
            'url': "<gmaps>",
            'body': "Available until <24h_time> (<time_left>)."
        },
        'stops': {
            'title': "Someone has placed a lure on a Pokestop!",
            'url': "<gmaps>",
            'body': "Lure will expire at <24h_time> (<time_left>)."
        },
        'gyms': {
            'title': "A Team <old_team> gym has fallen!",
            'url': "<gmaps>",
            'body': "It is now controlled by <new_team>."
        },
        'eggs': {
            'title': "A level <egg_lvl> raid is incoming!",
            'url': "<gmaps>",
            'body': "The egg will hatch <24h_hatch_time> (<hatch_time_left>)."
        },
        'raids': {
            'title': "Level <raid_lvl> raid is available against <mon_name>!",
            'url': "<gmaps>",
            'body': "The raid is available until <24h_raid_end>"
                    " (<raid_time_left>)."
        },
        'weather': {
            'title': "The weather has changed!",
            'url': "<gmaps>",
            'body': "The weather around <lat>,<lng> has changed to <weather>!"
        },
        'quests': {
            'title': '*New quest for <reward>*',
            'url': '<gmaps>',
            'body': '<quest_task>'
        },
        'invasions': {
            'title': 'A Pokestop has been invaded by Team Rocket!',
            'url': '<gmaps>',
            'body': 'Invasion will expire at <24h_time> (<time_left>).'
        }
    }

    # Gather settings and create alarm
    def __init__(self, mgr, settings):
        self._log = mgr.get_child_logger("alarms")

        # Required Parameters
        self.__api_key = require_and_remove_key(
            'api_key', settings, "'Pushbullet' type alarms.")
        self.__client = None
        self.__channels = {}

        # Optional Alarm Parameters
        self.__startup_message = parse_boolean(
            settings.pop('startup_message', "True"))
        self.__channel = settings.pop('channel', "True")
        self.__sender = None

        # Optional Alert Parameters
        self.__pokemon = self.create_alert_settings(
            settings.pop('monsters', {}), self._defaults['monsters'])
        self.__pokestop = self.create_alert_settings(
            settings.pop('stops', {}), self._defaults['stops'])
        self.__gym = self.create_alert_settings(
            settings.pop('gyms', {}), self._defaults['gyms'])
        self.__egg = self.create_alert_settings(
            settings.pop('eggs', {}), self._defaults['eggs'])
        self.__raid = self.create_alert_settings(
            settings.pop('raids', {}), self._defaults['raids'])
        self.__weather = self.create_alert_settings(
            settings.pop('weather', {}), self._defaults['weather'])
        self.__quest = self.create_alert_settings(
            settings.pop('quests', {}), self._defaults['quests'])
        self.__invasions = self.create_alert_settings(
            settings.pop('invasions', {}), self._defaults['invasions'])

        #  Warn user about leftover parameters
        reject_leftover_parameters(
            settings, "Alarm level in Pushbullet alarm.")

        # Prepare request session
        self._session = requests.Session()
        self._session.headers = {
            'Access-Token': self.__api_key,
            'Content-Type': 'application/json'
        }

        self._log.info("Pushbullet Alarm has been created!")

    # Establish connection with Pushbullet
    def connect(self):
        self.update_channels()
        self.__sender = self.get_sender(self.__channel)
        self.__pokemon['sender'] = self.get_sender(self.__pokemon['channel'])
        self.__pokestop['sender'] = self.get_sender(self.__pokestop['channel'])
        self.__gym['sender'] = self.get_sender(self.__gym['channel'])
        self.__egg['sender'] = self.get_sender(self.__egg['channel'])
        self.__raid['sender'] = self.get_sender(self.__raid['channel'])
        self.__weather['sender'] = self.get_sender(self.__weather['channel'])

    def startup_message(self):
        if self.__startup_message:
            args = {
                "sender": self.__sender,
                "title": "PokeAlarm activated!",
                "message": "PokeAlarm has successully started!"
            }
            try_sending(
                self._log, self.connect, "PushBullet", self.push_note, args)
            self._log.info("Startup message sent!")

    # Set the appropriate settings for each alert
    def create_alert_settings(self, settings, default):
        alert = {
            'title': settings.pop('title', default['title']),
            'url': settings.pop('url', default['url']),
            'body': settings.pop('body', default['body']),
            'channel': settings.pop('channel', None)
        }
        reject_leftover_parameters(
            settings, "Alert level in Pushbullet alarm.")
        return alert

    # Send Alert to Pushbullet
    def send_alert(self, alert, info):
        args = {
            'sender': alert['sender'],
            'title': replace(alert['title'], info),
            'url': replace(alert['url'], info),
            'body': replace(alert['body'], info)
        }
        try_sending(
            self._log, self.connect, "PushBullet", self.push_link, args)

    # Trigger an alert based on Pokemon info
    def pokemon_alert(self, pokemon_info):
        self.send_alert(self.__pokemon, pokemon_info)

    # Trigger an alert based on Pokestop info
    def pokestop_alert(self, pokestop_info):
        self.send_alert(self.__pokestop, pokestop_info)

    # Trigger an alert based on Gym info
    def gym_alert(self, gym_info):
        self.send_alert(self.__gym, gym_info)

    # Trigger an alert when a raid egg has spawned (UPCOMING raid event)
    def raid_egg_alert(self, raid_info):
        self.send_alert(self.__egg, raid_info)

    # Trigger an alert based on Gym info
    def raid_alert(self, raid_info):
        self.send_alert(self.__raid, raid_info)

    # Trigger an alert based on Weather info
    def weather_alert(self, weather_info):
        self.send_alert(self.__weather, weather_info)

    # Trigger quest alert
    def quest_alert(self, quest_info):
        self.send_alert(self.__quest, quest_info)

    # Trigger quest alert
    def invasion_alert(self, invasion_info):
        self.send_alert(self.__invasions, invasion_info)

    # Attempt to get the channel, otherwise default to all devices
    def get_sender(self, channel_tag):
        req_channel = next(
            (channel for channel in self.__channels
             if channel['tag'] == channel_tag), None)
        if req_channel is None and channel_tag is not None:
            self._log.error(
                "Unable to find channel. Pushing to all devices instead.")
        else:
            self._log.debug("Setting to channel %s." % channel_tag)
        return req_channel

    # Push a link to the given channel
    def push_link(self, sender, title, url, body):
        data = {"type": "link", "title": title, "url": url, "body": body}
        if sender is not None:
            data.update({'channel_tag': sender['tag']})
        self.push(data)

    # Push a link to the given channel
    def push_note(self, sender, title, message):
        data = {"type": "note", "title": title, "body": message}
        if sender is not None:
            data.update({'channel_tag': sender['tag']})
        self.push(data)

    def push(self, data):
        res = self._session.post(
            'https://api.pushbullet.com/v2/pushes', data=json.dumps(data))
        if res.status_code != requests.codes.ok:
            self._log.debug(f'PushBullet response was {res.content}')
            raise requests.exceptions.RequestException(
                f'Response received {res.status_code}, webhook not accepted.')

        self._log.debug('Notification successful '
                        f'(returned {res.status_code})')

    def update_channels(self):
        response = self._session.get(
            'https://api.pushbullet.com/v2/channels', timeout=30)
        if response.ok is not True:
            self._log \
                .debug(f'Pushbullet channels response was {response.content}')
            raise requests.exceptions.RequestException(
                f'Response received {response.status_code}, '
                'channel grabbing not successful')
        try:
            self.__channels = response.json()['channels']
        except KeyError:
            self._log.error('Problem with the PushBullet API')
            self._log.debug(
                f'PushBullet /v2/channels response:{response.json()}')
        self._log.debug('Detected the following PushBullet channels: {}'
                        .format(self.__channels))
