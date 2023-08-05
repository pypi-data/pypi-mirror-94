#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import logging
import GLXCurses


class HandlersEditable(object):

    def _handle_changed(self, event_signal, event_args=None):
        logging.debug(
            "{0}._handle_changed({1}, {2})".format(
                self.__class__.__name__, event_signal, event_args
            )
        )
        widget = GLXCurses.Application().get_widget_by_id(event_args["id"])
        pass

    def _handle_delete_text(self, event_signal, event_args=None):
        logging.debug(
            "{0}._handle_delete_text({1}, {2})".format(
                self.__class__.__name__, event_signal, event_args
            )
        )
        widget = GLXCurses.Application().get_widget_by_id(event_args["id"])
        pass

    def _handle_insert_text(self, event_signal, event_args=None):
        logging.debug(
            "{0}._handle_insert_text({1}, {2})".format(
                self.__class__.__name__, event_signal, event_args
            )
        )
        widget = GLXCurses.Application().get_widget_by_id(event_args["id"])
        pass
