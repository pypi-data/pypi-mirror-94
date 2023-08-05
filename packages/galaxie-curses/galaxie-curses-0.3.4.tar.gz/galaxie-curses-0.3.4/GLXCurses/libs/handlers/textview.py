#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import logging
import GLXCurses


class HandlersTextView:

    def _handle_backspace(self, event_signal, event_args=None):
        logging.debug("{0}._handle_backspace({1}, {2})".format(self.__class__.__name__,
                                                               event_signal,
                                                               event_args
                                                               )
                      )
        pass

    def _handle_copy_clipboard(self, event_signal, event_args=None):
        logging.debug("{0}._handle_copy_clipboard({1}, {2})".format(self.__class__.__name__,
                                                                    event_signal,
                                                                    event_args
                                                                    )
                      )
        pass

    def _handle_cut_clipboard(self, event_signal, event_args=None):
        logging.debug("{0}._handle_cut_clipboard({1}, {2})".format(self.__class__.__name__,
                                                                   event_signal,
                                                                   event_args
                                                                   )
                      )
        pass

    def _handle_delete_from_cursor(self, event_signal, event_args=None):
        logging.debug("{0}._handle_delete_from_cursor({1}, {2})".format(self.__class__.__name__,
                                                                        event_signal,
                                                                        event_args
                                                                        )
                      )
        pass

    def _handle_extend_selection(self, event_signal, event_args=None):
        logging.debug("{0}._handle_extend_selection({1}, {2})".format(self.__class__.__name__,
                                                                      event_signal,
                                                                      event_args
                                                                      )
                      )
        pass

    def _handle_insert_at_cursor(self, event_signal, event_args=None):
        logging.debug("{0}._handle_insert_at_cursor({1}, {2})".format(self.__class__.__name__,
                                                                      event_signal,
                                                                      event_args
                                                                      )
                      )
        pass

    def _handle_insert_emoji(self, event_signal, event_args=None):
        logging.debug("{0}._handle_insert_emoji({1}, {2})".format(self.__class__.__name__,
                                                                  event_signal,
                                                                  event_args
                                                                  )
                      )
        pass

    def _handle_move_cursor(self, event_signal, event_args=None):
        logging.debug("{0}._handle_move_cursor({1}, {2})".format(self.__class__.__name__,
                                                                 event_signal,
                                                                 event_args
                                                                 )
                      )
        pass

    def _handle_move_viewport(self, event_signal, event_args=None):
        logging.debug("{0}._handle_move_viewport({1}, {2})".format(self.__class__.__name__,
                                                                   event_signal,
                                                                   event_args
                                                                   )
                      )
        pass

    def _handle_paste_clipboard(self, event_signal, event_args=None):
        logging.debug("{0}._handle_paste_clipboard({1}, {2})".format(self.__class__.__name__,
                                                                     event_signal,
                                                                     event_args
                                                                     )
                      )
        pass

    def _handle_populate_popup(self, event_signal, event_args=None):
        logging.debug("{0}._handle_populate_popup({1}, {2})".format(self.__class__.__name__,
                                                                    event_signal,
                                                                    event_args
                                                                    )
                      )
        pass

    def _handle_preedit_changed(self, event_signal, event_args=None):
        logging.debug("{0}._handle_preedit_changed({1}, {2})".format(self.__class__.__name__,
                                                                     event_signal,
                                                                     event_args
                                                                     )
                      )
        pass

    def _handle_select_all(self, event_signal, event_args=None):
        logging.debug("{0}._handle_select_all({1}, {2})".format(self.__class__.__name__,
                                                                event_signal,
                                                                event_args
                                                                )
                      )
        pass

    def _handle_set_anchor(self, event_signal, event_args=None):
        logging.debug("{0}._handle_set_anchor({1}, {2})".format(self.__class__.__name__,
                                                                event_signal,
                                                                event_args
                                                                )
                      )
        pass

    def _handle_toggle_cursor_visible(self, event_signal, event_args=None):
        logging.debug("{0}._handle_toggle_cursor_visible({1}, {2})".format(self.__class__.__name__,
                                                                           event_signal,
                                                                           event_args
                                                                           )
                      )
        pass

    def _handle_toggle_overwrite(self, event_signal, event_args=None):
        logging.debug("{0}._handle_toggle_overwrite({1}, {2})".format(self.__class__.__name__,
                                                                      event_signal,
                                                                      event_args
                                                                      )
                      )
        pass
