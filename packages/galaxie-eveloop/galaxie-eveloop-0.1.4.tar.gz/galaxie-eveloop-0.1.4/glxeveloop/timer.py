#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import time, sleep
from queue import Queue
from glxeveloop.fps import FPS


# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Tuuux <tuxa at rtnp dot org> all rights reserved


# Reference Document: http://code.activestate.com/recipes/579053-high-precision-fps/
class Timer(object):
    SPEED_STEP_PERCENTAGE = 10
    DEFAULT_BE_FAST_MULTIPLICATOR = 100
    MIN_BE_FAST_MULTIPLICATOR = 0

    """
    :Description:

    The :class:`Timer <glxeveloop.timer.Timer>` object contain a self-correcting timing algorithms.

    That self-correcting timing algorithms have associated property's it permit to control the
    :class:`Timer <glxeveloop.timer.Timer>` object.

    The power saving happen that because the loop try to limit the number of mainloop cycle
    The :class:`Timer <glxeveloop.timer.Timer>` object update value itself and can be requested, via internal method's.
    """

    def __init__(self):
        # Internal
        self.__debug = None
        self.__queue = None
        self.__fps = None
        self.__time_departure = None
        self.__be_fast = None
        self.__be_fast_multiplicator = None

        # First Init
        self.debug = None
        self.fps = None
        self.be_fast = None
        self.be_fast_multiplicator = None
        self.position = 0
        self.queue = Queue(maxsize=10)
        # self.queue.maxsize = self.size

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
            if self.fps:
                self.fps.debug = self.debug

    @property
    def fps(self):
        """
        The FPS object

        :return: :py:data:`fps` property value. (in **fps**)
        :rtype: FPS
        """
        return self.__fps

    @fps.setter
    def fps(self, value=None):
        """
        Set the :class:`Timer <glxeveloop.timer.Timer>` :py:data:`fps` property.

        :param value: a FPS object
        :type value: FPS
        :raise TypeError: if ``fps`` parameter is not a  FPS instance
        """
        if value is None:
            value = FPS()
        if not isinstance(value, FPS):
            raise TypeError("'fps' property value must be a FPS instance")
        if self.fps != value:
            self.__fps = value

    @property
    def queue(self):
        """
        Store the Timer Buffer object.

        :return: TimerBuffer instance
        :rtype: Memory
        """
        return self.__queue

    @queue.setter
    def queue(self, value=None):
        if value is None:
            value = Queue()
        if not isinstance(value, Queue):
            raise TypeError("'queue' property value must be a Memory instance or None")
        if self.queue != value:
            self.__queue = value

    def tick(self):
        """
        Return :py:obj:`True` or :py:obj:`False` "when necessary" , that mean according with all the self-correcting
        timing algorithms and they configuration property's


        .. code-block:: python

           timer = Timer()
           while True:
               # Do stuff that might take significant time here

               if timer.tick():
                   print('Hello World!')

        :return: :py:obj:`True` when it's time or :py:obj:`False` if a adjustment job of :py:data:`fps` property
                 should be done
        :rtype: bool
        """
        if self.time_departure is None:
            self.time_departure = self.time

        # Increase position
        self.position += 1

        # The algorithm
        target = self.position / self.fps.value
        passed = self.time - self.time_departure
        differ = target - passed

        # Reset time reference due to time variation
        # Should never be remove or for a true system if compensate time variation
        if self.queue.full():
            self.time_departure = self.time
            self.position = 0

            # Determine a increment factor for fast convergence
            # half_sum = sum(self.queue.buffer[:len(self.queue.buffer) / 2])
            half_sum = 0.0
            rest_sum = 0.0
            orig_size = self.queue.qsize()

            while not self.queue.empty():
                if self.queue.qsize() <= int(orig_size / 2):
                    half_sum += self.queue.get()
                else:
                    rest_sum += self.queue.get()

            # It's time to analyze the result
            # First Check if that equal
            if int(half_sum) == int(rest_sum):
                self.be_fast_multiplicator = 0
                self.be_fast = False
                if self.debug:
                    logging.info(
                        "{0}:[GOAL]-> Increment {1} fps, {2} fps".format(
                            self.__class__.__name__,
                            self.fps.fps_increment,
                            self.fps.value,
                        )
                    )

            else:
                # Check if we have to down fps
                if half_sum < rest_sum:
                    if self.be_fast:
                        if self.debug:
                            logging.info(
                                "{0}:[DOWN]-> Increment {1} fps, {2} fps".format(
                                    self.__class__.__name__,
                                    self.fps_accelerated,
                                    self.fps.value,
                                )
                            )

                        self.be_fast_multiplicator -= self.SPEED_STEP_PERCENTAGE

                    else:
                        self.be_fast_multiplicator = None
                        if self.debug:
                            logging.info(
                                "{0}:[DOWN]-> Increment {1} fps, {2} fps".format(
                                    self.__class__.__name__,
                                    self.fps.fps_increment,
                                    self.fps.value,
                                )
                            )
                    self.be_fast = False

                elif half_sum > rest_sum:
                    # Everything is fine , yes we can
                    if self.be_fast:
                        if self.debug:
                            logging.info(
                                "{0}:[UP]-> Increment {1} fps, {2} fps".format(
                                    self.__class__.__name__,
                                    self.fps_accelerated,
                                    self.fps.value,
                                )
                            )
                        self.be_fast_multiplicator += self.SPEED_STEP_PERCENTAGE

                    else:
                        if self.debug:
                            logging.info(
                                "{0}:[UP]-> Increment {1} fps, {2} fps".format(
                                    self.__class__.__name__,
                                    self.fps.fps_increment,
                                    self.fps.value,
                                )
                            )
                        self.be_fast_multiplicator = None

                    self.be_fast = True

        # Monitor the frame fps
        self.queue.put(self.fps.value)

        # Now we know how many time differ from the ideal Frame Rate
        if differ <= 0:
            # raise ValueError('cannot maintain desired FPS fps')
            if self.be_fast:
                self.fps.value -= (
                    self.fps.fps_max_increment * self.be_fast_multiplicator / 100
                )
            else:
                self.fps.value -= self.fps.fps_increment
            # Return False that because we haven't respect the ideal frame fps
            return False
        else:
            if self.be_fast:
                self.fps.value += (
                    self.fps.fps_max_increment * self.be_fast_multiplicator / 100
                )
            else:
                self.fps.value += self.fps.fps_increment

            # Everything is fine , we have spare time then we can sleep for the rest of the frame time
            sleep(differ)
            # Return True that because we have respect the ideal frame fps
            return True

    @property
    def fps_accelerated(self):
        return (self.fps.fps_max_increment * self.be_fast_multiplicator) / 100

    @property
    def time(self):
        """
        Time should be take as a serious thing, you should try to impose only one time source in you program, then the
        :class:`Timer <glxeveloop.timer.Timer>` Class provide it own method for get the time by it self.

        :return: Unix time
        :rtype: int
        """
        return time()

    @property
    def time_departure(self):
        """
        Return the value set by a :func:`Timer._set_departure_time() <glxeveloop.timer.Timer._set_departure_time()>`

        :return: return :py:data:`departure_time` property.
        :rtype: Unix time
        """
        return self.__time_departure

    @time_departure.setter
    def time_departure(self, time_value=None):
        """
        Store a :func:`Timer.get_time() <glxeveloop.timer.Timer.get_time()>` return value inside
        :py:data:`departure_time` property.

        :param time_value: return value inside :py:data:`departure_time` property.
        :type time_value: float
        """
        if time_value and type(time_value) != float:
            raise TypeError("'time_value' property value must be a float type or None")
        if self.time_departure != time_value:
            self.__time_departure = time_value

    @property
    def be_fast(self):
        """
        Return the value set by :func:`Timer._set_be_fast() <glxeveloop.timer.Timer._set_be_fast()>` method.

        You can set :py:attr:`__be_fast` property with

        :func:`Timer._set_be_fast() <glxeveloop.timer.Timer._set_be_fast()>` method.
        :return: :py:attr:`__be_fast` property
        :rtype: bool
        """
        return self.__be_fast

    @be_fast.setter
    def be_fast(self, be_fast=None):
        """
        Set the __be_fast property after have check if teh value is different and if type is a boolean value like:
        True, False, O, 1

        That value will be use for fast convergence, when the Timer search for the best Frame fps

        :param be_fast:
        :type be_fast: bool
        :raise TypeError: if ``be_fast`` parameter is not a :py:data:`bool` type
        """
        if be_fast is None:
            be_fast = False
        if type(be_fast) != bool:
            raise TypeError(u">be_fast< parameter must be a bool")
        if self.be_fast is not be_fast:
            self.__be_fast = be_fast

    @property
    def be_fast_multiplicator(self):
        """
        Return the be_fast_multiplicator property value

        :return: :py:attr:`__be_fast_multiplicator` property
        :rtype: int
        """
        return self.__be_fast_multiplicator

    @be_fast_multiplicator.setter
    def be_fast_multiplicator(self, value=None):
        """
        Set the :py:attr:`be_fast_multiplicator` property

        That value will be use for fast convergence, when the Timer search for the best Frame fps

        :param value:
        :type value: int
        :raise TypeError: if ``be_fast_multiplicator``  property value is is not a :py:data:`int` type or None
        """
        if value is None:
            value = 10
        if type(value) != int:
            raise TypeError("'be_fast' parameter must be a int")
        if self.be_fast_multiplicator != value:
            self.__be_fast_multiplicator = value
