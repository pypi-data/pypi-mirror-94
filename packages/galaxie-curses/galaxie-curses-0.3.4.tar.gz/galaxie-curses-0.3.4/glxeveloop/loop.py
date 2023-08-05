#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie EveLoop Team, all rights reserved

import sys
import logging

import threading

# lock = threading.Lock()
from glxeveloop.events import Events
from glxeveloop.hooks import Hooks
from glxeveloop.timer import Timer


class Singleton(type):
    def __init__(cls, name, bases, dictionary):
        super(Singleton, cls).__init__(name, bases, dictionary)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


# https://developer.gnome.org/glib/stable/glib-The-Main-Event-Loop.html
class Loop(object, metaclass=Singleton):
    """
    :Description:

    The Loop is something close to a infinity loop with a start() and stop() method
        * Parse user input into a Statement object
        * Start timer
        * Call precmd method
        * Add statement to History
        * Call cmd method
        * Call postcmd method
        * Stop timer and display the elapsed time
        * In Case of Exit call methods loop_finalization

    .. warning:: You have to start the mainloop from the application with ``Loop.start()`` function.
    """

    def __init__(self):
        """
        Creates a new Loop structure.
        """
        self.__debug = None
        self.__hooks = None
        self.__timer = None
        self.__events = None
        self.__running = None

        # First init
        self.debug = None
        self.hooks = None
        self.events = None
        self.timer = None
        self.running = None

    @property
    def debug(self):
        return self.__debug

    @debug.setter
    def debug(self, value=None):
        """
        Set the debugging level of information's display on the stdout.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param value: True is debugging mode is enable, False for disable it.
        :type value: bool
        :raise TypeError: when "debug" argument is not a :py:__area_data:`bool`
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"debug" property value must be a boolean type or None')
        if self.debug != value:
            self.__debug = value

    @property
    def hooks(self):
        return self.__hooks

    @hooks.setter
    def hooks(self, value):
        if value is None:
            value = Hooks()
        if not isinstance(value, Hooks):
            raise TypeError(
                "'hooks' property value must be a Hooks instance or None"
            )
        if value != self.hooks:
            self.__hooks = value
            self.hooks.debug = self.debug

    @property
    def timer(self):
        return self.__timer

    @timer.setter
    def timer(self, value):
        if value is None:
            value = Timer()
        if not isinstance(value, Timer):
            raise TypeError(
                "'timer' property value must be a Timer instance or None"
            )
        if self.timer != value:
            self.__timer = value
            self.timer.debug = self.debug

    @property
    def events(self):
        return self.__events

    @events.setter
    def events(self, value):
        if value is None:
            value = Events(debug=self.debug)
        if not isinstance(value, Events):
            raise TypeError(
                "'events' property value must be a Events instance or None"
            )
        if value != self.events:
            self.__events = value

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, value):
        """
        Set the is_running attribute

        :param value: False or True
        :type value: Boolean
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError("'running' property value must be bool type or None")
        if self.running != value:
            self.__running = value

    def start(self):
        """
        Runs a Loop until ``Mainloop.stop()`` is called on the loop. If this is called for the thread of the loop's
        , it will process events from the loop, otherwise it will simply wait.

            * Parse user input into a Statement object
            * Start timer
            * Call precmd method
            * Add statement to History
            * Call cmd method
            * Call postcmd method
            * Stop timer and display the elapsed time
            * In Case of Exit call methods loop_finalization
        """
        if self.debug:
            logging.debug("Starting " + self.__class__.__name__)
        self.running = True

        # Normally it the first refresh of the application, it can be considered as the first stdscr display.
        # Consider a chance to crash before the start of the loop
        try:
            # PRE
            if self.hooks.pre:
                self.hooks.pre()

            self.handle_event()

            # CMD
            if self.hooks.cmd:
                self.hooks.cmd()

            # POST
            if self.hooks.post:
                self.hooks.post()

        except Exception:
            self.stop()
            sys.stdout.write("{0}\n".format(sys.exc_info()[0]))
            sys.stdout.flush()
            raise

        # A bit light for notify about we are up and running, but we are really inside the main while(1) loop
        if self.debug:
            logging.debug(self.__class__.__name__ + ": Started")
        # The loop
        while self.running:
            # Parse user input into a Statement object
            # Start timer
            # Call loop_precmd method
            # Add statement to History
            # Call loop_cmd method
            # Call loop_postcmd method
            # Stop timer and display the elapsed time
            # In Case of Exit
            #   Call methods loop_finalization

            try:

                if self.hooks.statement:
                    self.hooks.statement()

                # PRE
                if self.hooks.pre:
                    self.hooks.pre()

                self.handle_event()

                # CMD
                if self.hooks.cmd:
                    self.hooks.cmd()

                # POST
                if self.hooks.post:
                    self.hooks.post()

                try:
                    self.timer.tick()
                except TypeError:  # pragma: no cover
                    pass

            except KeyboardInterrupt:  # pragma: no cover
                if self.hooks.keyboard_interruption:
                    self.hooks.keyboard_interruption()
                else:
                    self.stop()

            except Exception:  # pragma: no cover
                self.stop()
                sys.stdout.write("{0}\n".format(sys.exc_info()[0]))
                sys.stdout.flush()
                raise

        # running property have been set to False during a loop iteration
        # if hasattr(self.application, "eveloop_finalization"):
        if self.hooks.finalization:

            if self.debug:
                logging.debug(self.__class__.__name__ + ": Call finalization method")

            self.hooks.finalization()

        if self.debug:
            logging.debug(self.__class__.__name__ + ": All operations is stop")

    def stop(self):
        """
        Stops a Loop from running. Any calls to run() for the loop will return.

        Note that sources that have already been dispatched when quit() is called will still be executed.

        .. :warning: A Loop quit() call will certainly cause the end of you programme
        """
        if self.debug:
            logging.debug(self.__class__.__name__ + ": Stopping")

        self.running = False

    def handle_event(self):
        event = self.events.pop()
        try:
            if event:
                handler_list = []
                while event:

                    if self.hooks.dispatch:
                        if self.debug:
                            logging.debug("{3}.handle_event ({0}, {1}) to {2}".format(event[0],
                                                                                      event[1],
                                                                                      self.hooks.dispatch,
                                                                                      self.__class__.__name__)
                                          )
                        handler_list.append(threading.Thread(target=self.hooks.dispatch(event[0], event[1])))

                    event = self.events.pop()
                for handler in handler_list:
                    handler.start()
                for handler in handler_list:
                    handler.join()

        except KeyError as the_error:  # pragma: no cover
            # Permit to have error logs about unknown event
            logging.error(
                "{0}._handle_event(): KeyError:{1} event:{2}".format(
                    self.__class__.__name__, the_error, event
                )
            )
