#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie EveLoop Team, all rights reserved

from glxeveloop.loop import Loop
import threading


class Bus(object):
    """
    :Description:

    The ``EventBusClient`` object is The bus it interconnect Widget
    """

    def __init__(self, debug=None):

        # Public attribute
        self.__debug = None
        self.__subscriptions = None

        self.debug = debug
        self.subscriptions = None

    @property
    def debug(self):
        return self.__debug

    @debug.setter
    def debug(self, debug=None):
        """
        Set the debugging level of information's display on the stdscr.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param debug: True is debugging mode is enable, False for disable it.
        :type debug: bool
        :raise TypeError: when "debug" argument is not a :py:__area_data:`bool`
        """
        if debug is None:
            debug = False
        if type(debug) != bool:
            raise TypeError('"debug" must be a boolean type')
        if self.debug != debug:
            self.__debug = debug

    @property
    def subscriptions(self):
        """
        Return the subscriptions list

        :return: event buffer
        :rtype: dict
        """
        return self.__subscriptions

    @subscriptions.setter
    def subscriptions(self, value):
        if value is None:
            value = {}
        if type(value) != dict:
            raise TypeError("'subscriptions' property value must be dict type or None")
        if value != self.subscriptions:
            self.__subscriptions = value

    def connect(self, detailed_signal: object, handler: object, *args: object):
        """
        The connect() method adds a function or method (handler) to the end of the event list
        for the named detailed_signal but before the default class signal handler.
        An optional set of parameters may be specified after the handler parameter.
        These will all be passed to the signal handler when invoked.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param handler: a function handler
        :type handler: handler
        :param args: additional parameters arg1, arg2
        :type args: tuple
        """

        # If args is still None replace it by a empty list
        # if args is None:
        #     args = []

        # If detailed_signal is not in the event list create it
        if detailed_signal not in self.subscriptions:
            self.subscriptions[detailed_signal] = list()

        self.subscriptions[detailed_signal].append(handler)

        if args:
            self.subscriptions[detailed_signal].append(args)

    def disconnect(self, detailed_signal, handler):
        """
        The disconnect() method removes the signal handler with the specified handler
        from the list of signal handlers for the object.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param handler: a function handler
        :type handler: handler
        """
        if detailed_signal in self.subscriptions and handler in self.subscriptions[detailed_signal]:
            del (self.subscriptions[detailed_signal])

    @staticmethod
    def emit(detailed_signal, args):
        """
        Emit signal in direction to the Mainloop.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param args: additional parameters arg1, arg2
        :type args: dict
        """
        Loop().events.add(detailed_signal, args)

    def events_flush(self, detailed_signal, args):
        if detailed_signal in self.subscriptions:
            handler_list = []
            for handler in self.subscriptions[detailed_signal]:
                handler_list.append(threading.Thread(target=handler(self, detailed_signal, args)))
            for handler in handler_list:
                handler.start()
            for handler in handler_list:
                handler.join()

    def events_dispatch(self, detailed_signal, args):
        """
        Flush Mainloop event to Child's father's for a Widget's recursive event dispatch

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param args: additional parameters arg1, arg2
        """
        self.events_flush(detailed_signal, args)

        if hasattr(self, "eveloop_dispatch"):
            self.eveloop_dispatch(detailed_signal, args)
