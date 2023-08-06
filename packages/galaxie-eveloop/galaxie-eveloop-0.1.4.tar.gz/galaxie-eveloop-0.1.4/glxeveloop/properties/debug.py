#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie EveLoop Team, all rights reserved


class DebugProperty(object):
    def __init__(self):
        self.__debug = False

    @property
    def debug(self):
        return self.__debug

    @debug.setter
    def debug(self, value=None):
        """
        Set the debugging level of information's.

        Generally it highly stress the console and is here for future maintenance of that Application.

        :param value: True is debugging mode is enable, False for disable it.
        :type value: bool
        :raise TypeError: when "debug" argument is not a :py:__area_data:`bool`
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"debug" must be a boolean type or None')
        if self.debug != value:
            self.__debug = value
