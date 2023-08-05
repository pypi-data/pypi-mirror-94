import logging


class EventList(object):
    def __init__(self, buffer=None, debug=None):
        self.__buffer = None
        self.__debug = None

        self.buffer = buffer
        self.debug = debug

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
    def buffer(self):
        """
        Return the event_buffer list attribute, it lis can be edited or modify as you need

        :return: event buffer
        :rtype: list()
        """
        return self.__buffer

    @buffer.setter
    def buffer(self, value):
        if value is None:
            value = []
        if type(value) != list:
            raise TypeError("'buffer' property value must be list type or None")
        if value != self.buffer:
            self.__buffer = value

    def add(self, signal, args):
        """
        Emit a signal, it consist to add the signal structure inside a global event list

        :param signal: a string containing the signal name
        :param args: additional parameters arg1, arg2
        """
        if self.debug:
            logging.debug(self.__class__.__name__ + ": " + signal + " " + str(args))

        self.buffer.insert(0, [signal, args])

    def pop(self):
        if self.buffer:
            return self.buffer.pop()
