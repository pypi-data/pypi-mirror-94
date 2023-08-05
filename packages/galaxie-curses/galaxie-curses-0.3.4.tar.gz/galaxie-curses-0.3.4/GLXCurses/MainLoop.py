#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import sys
import logging

import threading

lock = threading.Lock()
from GLXCurses.EventList import EventList


class Singleton(type):
    def __init__(cls, name, bases, dictionary):
        super(Singleton, cls).__init__(name, bases, dictionary)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


# https://developer.gnome.org/glib/stable/glib-The-Main-Event-Loop.html
class MainLoop(object, metaclass=Singleton):
    """
    :Description:

    The MainLoop is something close to a infinity loop with a start() and stop() method

    Methods:
        start()            -- start the mainloop
        stop()             -- stop the mainloop
        emit()             -- emit a signal

    .. warning:: you have to start the mainloop from you application via MainLoop().start()
    """

    def __init__(self, application=None, debug=None):
        """
        Creates a new MainLoop structure.
        """
        self.__application = None
        self.__debug = None
        self.__event_list = None
        self.__running = None
        self.__glxcurses_support = None

        # First init
        self.application = application
        self.debug = debug
        self.event_list = None
        self.glxcurses_support = None

        self.running = None
        self.debug = True

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
    def application(self):
        return self.__application

    @application.setter
    def application(self, value):
        if value != self.application:
            self.__application = value

    @property
    def event_list(self):
        return self.__event_list

    @event_list.setter
    def event_list(self, value):
        if value is None:
            value = EventList(debug=self.debug)
        if not isinstance(value, EventList):
            raise TypeError("'event_list' property value must be a EventList instance or None")
        if value != self.event_list:
            self.__event_list = value

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

    @property
    def glxcurses_support(self):
        return self.__glxcurses_support

    @glxcurses_support.setter
    def glxcurses_support(self, value):
        """
        Set the glxcurses_support attribute

        :param value: If ``True`` the support for GLXCurses is enable
        :type value: Boolean
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError("'glxcurses_support' property value must be bool type or None")
        if self.glxcurses_support != value:
            self.__glxcurses_support = value

    def start(self):
        """
        Runs a MainLoop until quit() is called on the loop. If this is called for the thread of the loop's
        , it will process events from the loop, otherwise it will simply wait.
        """
        if self.debug:
            logging.debug("Starting " + self.__class__.__name__)
        self.running = True

        # Normally it the first refresh of the application, it can be considered as the first stdscr display.
        # Consider a chance to crash before the start of the loop
        try:
            self.handle_event()

            if hasattr(self.application, "eveloop_precmd"):
                self.application.eveloop_precmd()

            if hasattr(self.application, "eveloop_cmd"):
                self.application.eveloop_cmd()

            if hasattr(self.application, "eveloop_postcmd"):
                self.application.eveloop_postcmd()

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
                # Parse input event
                if hasattr(self.application, "eveloop_input_event"):
                    self.handle_event(self.application.eveloop_input_event())

                if hasattr(self.application, "eveloop_precmd"):
                    self.application.eveloop_precmd()

                if hasattr(self.application, "eveloop_cmd"):
                    self.application.eveloop_cmd()

                if hasattr(self.application, "eveloop_postcmd"):
                    self.application.eveloop_postcmd()

            except KeyboardInterrupt:

                # Default EvLoop Keyboard Interruption
                if hasattr(self.application, "permit_keyboard_interruption"):
                    if self.application.permit_keyboard_interruption:
                        self.stop()
                        sys.stdout.write("{0}: {1}\n".format("KeyboardInterrupt", sys.exc_info()[2]))
                        sys.stdout.flush()
                    else:
                        if self.glxcurses_support:
                            self.event_list.add("CURSES", 3)
                else:
                    self.stop()
                    sys.stdout.write("{0}: {1}\n".format("KeyboardInterrupt", sys.exc_info()[2]))
                    sys.stdout.flush()

            except Exception:
                self.stop()
                sys.stdout.write("{0}\n".format(sys.exc_info()[0]))
                sys.stdout.flush()
                raise

        # running property have been set to False during a loop iteration
        if hasattr(self.application, "eveloop_finalization"):

            if self.debug:
                logging.debug(self.__class__.__name__ + ": Call finalization method")

            self.application.eveloop_finalization()

        if self.debug:
            logging.debug(self.__class__.__name__ + ": All operations is stop")

    def stop(self):
        """
        Stops a MainLoop from running. Any calls to run() for the loop will return.

        Note that sources that have already been dispatched when quit() is called will still be executed.

        .. :warning: A MainLoop quit() call will certainly cause the end of you programme
        """
        if self.debug:
            logging.debug(self.__class__.__name__ + ": Stopping")

        self.running = False

    def handle_event(self, event=None):

        # GLXCurses Support
        if self.glxcurses_support:
            # curses.getch() event support
            if event != -1:
                # curses.mouse event
                if event == 409:
                    # get mouse position from GLXCurses.Application() class
                    if hasattr(self.application, "get_mouse"):
                        self.event_list.add("MOUSE_EVENT", self.application.get_mouse())
                # curses event
                else:
                    self.event_list.add("CURSES", event)

        # Default EvLoop mode
        else:
            if event:
                self.event_list.add("EVENT", event)

        # Do something with events
        event = self.event_list.pop()
        try:
            if event:
                while event:
                    # If it have event dispatch it
                    if self.debug:
                        logging.debug("{0}: Dispatch {1}: {2} to self.application".format(
                            self.__class__.__name__, event[0], event[1]))

                    # Dispatch to the application
                    if hasattr(self.application, "events_dispatch"):
                        self.application.events_dispatch(event[0], event[1])

                    # Delete the last event inside teh event list
                    event = self.event_list.pop()

        except KeyError as the_error:
            # Permit to have error logs about unknown event
            logging.error(
                "{0}._handle_event(): KeyError:{1} event:{2}".format(
                    self.__class__.__name__, the_error, event
                )
            )
