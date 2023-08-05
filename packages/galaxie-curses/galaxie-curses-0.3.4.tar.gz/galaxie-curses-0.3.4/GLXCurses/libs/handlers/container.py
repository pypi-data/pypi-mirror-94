#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import logging
import GLXCurses


class HandlersContainer(object):

    def _handle_add(self, event_signal, event_args=None):
        logging.debug(
            "{0}._handle_add({1}, {2})".format(
                self.__class__.__name__, event_signal, event_args
            )
        )

        GLXCurses.Application().active_widgets.append(
            GLXCurses.ChildElement(
                widget=event_args["widget"],
                widget_id=event_args["id"],
            )
        )

    def _handle_check_resize(self, event_signal, event_args=None):
        logging.debug(
            "{0}._handle_check_resize({1}, {2})".format(
                self.__class__.__name__, event_signal, event_args
            )
        )
        pass

    def _handle_remove(self, event_signal, event_args=None):
        logging.debug(
            "{0}._handle_remove({1}, {2})".format(
                self.__class__.__name__, event_signal, event_args
            )
        )
        pass

    def _handle_set_focus_child(self, event_signal, event_args=None):
        logging.debug(
            "{0}._handle_set_focus_child({1}, {2})".format(
                self.__class__.__name__, event_signal, event_args
            )
        )
        pass
