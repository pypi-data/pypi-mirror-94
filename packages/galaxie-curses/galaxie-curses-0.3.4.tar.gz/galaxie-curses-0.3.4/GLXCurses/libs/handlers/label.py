#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import logging
import GLXCurses


class HandlersLabel:

    def _handle_activate_current_link(self, event_signal, event_args=None):
        """
        A keybinding signal which gets emitted when the user activates a link in the label.

        Applications may also emit the signal with g_signal_emit_by_name() if they need to control activation of URIs programmatically.

        The default bindings for this signal are all forms of the Enter key.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data
        :type event_args: dict
        """
        logging.debug("{0}._handle_activate_current_link({1}, {2})".format(self.__class__.__name__,
                                                                           event_signal,
                                                                           event_args
                                                                           )
                      )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        pass

    def _handle_activate_link(self, event_signal, event_args=None):
        """
        The signal which gets emitted to activate a URI.

        Applications may connect to it to override the default behaviour, which is to call show_uri_on_window().

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data
        :type event_args: dict
        """
        logging.debug("{0}._handle_activate_link({1}, {2})".format(self.__class__.__name__,
                                                                   event_signal,
                                                                   event_args
                                                                   )
                      )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        pass

    def _handle_copy_clipboard(self, event_signal, event_args=None):
        """
        The ::copy-clipboard signal is a keybinding signal which gets emitted to copy the selection to the clipboard.

        The default binding for this signal is Ctrl-c.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data
        :type event_args: dict
        """
        logging.debug("{0}._handle_copy_clipboard({1}, {2})".format(self.__class__.__name__,
                                                                    event_signal,
                                                                    event_args
                                                                    )
                      )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        pass

    def _handle_move_cursor(self, event_signal, event_args=None):
        """
        The ::move-cursor signal is a keybinding signal which gets emitted when the user initiates a cursor movement.
        If the cursor is not visible in entry , this signal causes the viewport to be moved instead.

        Applications should not connect to it, but may emit it with g_signal_emit_by_name()
        if they need to control the cursor programmatically.

        The default bindings for this signal come in two variants, the variant with the Shift modifier
        extends the selection, the variant without the Shift modifer does not.

        There are too many key combinations to list them all here.

        Arrow keys move by individual characters/lines

        Ctrl-arrow key combinations move by words/paragraphs

        Home/End keys move to the ends of the buffer

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data
        :type event_args: dict
        """
        logging.debug("{0}._handle_move_cursor({1}, {2})".format(self.__class__.__name__,
                                                                 event_signal,
                                                                 event_args
                                                                 )
                      )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        pass

    def _handle_populate_popup(self, event_signal, event_args=None):
        """
        The ::populate-popup signal gets emitted before showing the context menu of the label.
        Note that only selectable labels have context menus.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data
        :type event_args: dict
        """
        logging.debug("{0}._handle_populate_popup({1}, {2})".format(self.__class__.__name__,
                                                                    event_signal,
                                                                    event_args
                                                                    )
                      )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        pass
