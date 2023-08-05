#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import logging
import GLXCurses


class HandlersButton:

    def _handle_activate(self, event_signal, event_args=None):
        """
        The ::activate signal on GLXCurses.Button is an action signal and emitting it causes the button to animate
        press then release.

        Applications should never connect to this signal, but use the “clicked” signal.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data
        :type event_args: dit
        """
        logging.debug("{0}._handle_activate({1}, {2})".format(self.__class__.__name__,
                                                              event_signal,
                                                              event_args
                                                              )
                      )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        if hasattr(widget, 'active'):
            widget.active = not widget.active

    def _handle_clicked(self, event_signal, event_args=None):
        logging.debug("{0}._handle_clicked({1}, {2})".format(self.__class__.__name__,
                                                             event_signal,
                                                             event_args
                                                             )
                      )
        pass

