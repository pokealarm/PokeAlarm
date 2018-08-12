# -*- coding: utf-8 -*-

"""
PokeAlarm Prototype Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a prototype library for PokeAlarm.
"""

# Standard Library Imports
from __future__ import absolute_import, unicode_literals
import os
# 3rd Party Imports
# Local Imports

_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class Unknown:
    """ Enum for unknown DTS. """
    TINY = '?'
    SMALL = '???'
    REGULAR = 'unknown'
    EMPTY = ''

    __unknown_set = {TINY, SMALL, REGULAR}

    @classmethod
    def is_(cls, *args):
        """ Returns true if any given arguments are unknown, else false """
        for arg in args:
            if arg in cls.__unknown_set:
                return True
        return False

    @classmethod
    def is_not(cls, *args):
        """ Returns false if any given arguments are unknown, else true """
        for arg in args:
            if arg in cls.__unknown_set:
                return False
        return True

    @classmethod
    def or_empty(cls, val, default=EMPTY):
        """ Returns an default if unknown, else the original value. """
        return val if val not in cls.__unknown_set else default
