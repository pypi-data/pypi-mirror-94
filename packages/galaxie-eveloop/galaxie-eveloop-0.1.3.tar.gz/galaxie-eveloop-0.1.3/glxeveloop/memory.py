#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Tuuux <tuxa at rtnp dot org> all rights reserved


class Memory(object):
    """
    The Memory class as the role to keep a trace of time take by each iteration of the Loop.

    It class is use by the Loop, and a object instance is store in Mainloop in a property call ``memory``
    """

    def __init__(self):
        # Hidden
        self.__size = None
        self.__buffer = None
        self.__position = None

        # First init
        self.size = None
        self.buffer = None
        self.position = None

    def add(self, value):
        """
        The add function, permit to insert a ``value`` at the beginning of the :py:data:`buffer` property list
        and assure the :py:data:`buffer` list size is not superior to :py:data:`size` property.

        .. note:: It have no method to remove a added value.

        :param float value: The value value to add to the :py:data:`buffer` property list
        :rtype TypeError: When ``value`` parameter is not a :py:data:`float` type or :py:obj:`None`
        """
        if type(value) != float:
            raise TypeError("'add' parameter value must be a float type")

        self.buffer.insert(0, value)

        while len(self.buffer) > self.size:
            del self.buffer[-1]

    @property
    def buffer(self):
        """
        The :py:data:`buffer` property is use to keep a short memory of the Loop iteration time.

        The property return the :py:data:`buffer` property value, it consist to a :py:obj:`list` , with a specific
        size set by the :py:data:`size` property.

        Each element of the buffer list contain a :py:data:`float` object it reflet last iteration time of the Loop.

        The good way is to use :func:`Memory.add() <glxeveloop.Memory.add()>` to add, a value inside teh buffer.

        :return: :py:data:`buffer` property value
        :rtype: :py:data:`list` of :py:data:`float`
        :raise TypeError:
            if :py:attr:`buffer` property value is not set a :py:data:`list` type or :py:obj:`None`
        :raise ValueError:
            if :py:attr:`buffer` property value is not set with :py:data:`list` of :py:data:`float`
        """
        return self.__buffer

    @buffer.setter
    def buffer(self, value):
        """
        Set the :py:data:`buffer` property value

        :param value: list or None if want to reset the list
        :type value: list or None
        :raise TypeError: if ``buffer`` property value is not a :py:data:`list` type or :py:obj:`None`
        """
        if value is None:
            value = [None] * self.size
        if type(value) != list:
            raise TypeError("'buffer' property value must be a list type or None")
        for item in value:
            if item is not None and type(item) != float:
                raise ValueError("'buffer' property value must be a list of float type or None")
        if self.buffer != value:
            self.__buffer = value
            while len(self.buffer) <= self.size + 1:
                self.buffer.insert(0, self.buffer[-1])
            while len(self.buffer) > self.size:
                del self.buffer[-1]

    @property
    def position(self):
        """
        :py:attr:`position` property correspond to a cursor position inside :py:attr:`buffer` property list.

        Ideally when :func:`Loop.start() <glxeveloop.Loop.start()>` is call the value
        of :py:attr:`position` property should be set to ``0``

        .. rubric:: Exemples

        Use the setter and the getter

        >>> from glxeveloop import Memory
        >>> memory = Memory()

        >>> memory.position = 42
        >>> print(memory.position)
        42

        Restore the default value

        >>> memory.position = None
        >>> print(memory.position)
        0

        Type defensive propection

        >>> memory.position = 'Hello'
        TypeError: 'position' property value must be a int type or None

        :return: The cursor position inside the :py:attr:`buffer` property list
        :rtype: :py:data:`int`
        :raise TypeError: if :py:attr:`position` property value is not a :py:data:`int` type or :py:obj:`None`
        """
        return self.__position

    @position.setter
    def position(self, value=None):
        """
        Set the ``position`` property

        :param value: correspond to the position inside ``buffer`` property list
        :type value: int
        :raise TypeError: if :py:attr:`position` property value is not a :py:data:`int` type or :py:obj:`None`
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError("'position' property value must be a int type or None")
        if self.position != value:
            self.__position = value

    @property
    def size(self):
        """
        Get the :class:`Memory <glxeveloop.memory.Memory>` :py:attr:`size` property.

        It will be use as buffer during Loop calculation.

        .. rubric:: Exemples

        >>> from glxeveloop import Memory

        Use the setter and the getter

        >>> memory = Memory()
        >>> memory.size = 42
        >>> print(memory.size)
        42

        Restore the default value

        >>> memory = Memory()
        >>> memory.size = None
        >>> print(memory.size)
        10

        Type defensive propection

        >>> memory = Memory()
        >>> memory.size = 'Hello'
        TypeError: 'size' property value must be a int type or None

        :return: :py:attr:`size` property value
        :rtype: :py:data:`int`
        :raise TypeError: if :py:attr:`size` property value is not set with a :py:data:`int` type or :py:obj:`None`
        """
        return self.__size

    @size.setter
    def size(self, value=None):
        """
        Set the size property value

        :param value: correspond to the buffer size
        :type value: int
        :raise TypeError: if :py:attr:`size` property value is not a :py:data:`int` type or :py:obj:`None`
        """
        if value is None:
            value = 10
        if type(value) != int:
            raise TypeError("'size' property value must be a int type or None")
        if self.size != value:
            self.__size = value
            if self.buffer:
                while len(self.buffer) < self.size:
                    self.buffer.insert(0, self.buffer[-1])
                while len(self.buffer) > self.size:
                    del self.buffer[-1]
