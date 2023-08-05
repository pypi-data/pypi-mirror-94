#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import logging
import GLXCurses


class HandlersWidget:

    def _handle_accel_closures_changed(self, event_signal, event_args=None):
        logging.debug("{0}._handle_accel_closures_changed({1}, {2})".format(self.__class__.__name__,
                                                                            event_signal,
                                                                            event_args
                                                                            )
                      )
        pass

    def _handle_button_press_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_button_press_event({1}, {2})".format(self.__class__.__name__,
                                                                        event_signal,
                                                                        event_args
                                                                        )
                      )
        pass

    def _handle_button_release_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_button_release_event({1}, {2})".format(self.__class__.__name__,
                                                                          event_signal,
                                                                          event_args
                                                                          )
                      )
        pass

    def _handle_can_activate_accel(self, event_signal, event_args=None):
        logging.debug("{0}._handle_can_activate_accel({1}, {2})".format(self.__class__.__name__,
                                                                        event_signal,
                                                                        event_args
                                                                        )
                      )
        pass

    def _handle_child_notify(self, event_signal, event_args=None):
        logging.debug("{0}._handle_child_notify({1}, {2})".format(self.__class__.__name__,
                                                                  event_signal,
                                                                  event_args
                                                                  )
                      )
        pass

    def _handle_composited_changed(self, event_signal, event_args=None):
        logging.debug("{0}._handle_composited_changed({1}, {2})".format(self.__class__.__name__,
                                                                        event_signal,
                                                                        event_args
                                                                        )
                      )
        pass

    def _handle_configure_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_configure_event({1}, {2})".format(self.__class__.__name__,
                                                                     event_signal,
                                                                     event_args
                                                                     )
                      )
        pass

    def _handle_damage_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_damage_event({1}, {2})".format(self.__class__.__name__,
                                                                  event_signal,
                                                                  event_args
                                                                  )
                      )
        pass

    def _handle_delete_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_delete_event({1}, {2})".format(self.__class__.__name__,
                                                                  event_signal,
                                                                  event_args
                                                                  )
                      )
        pass

    def _handle_destroy(self, event_signal, event_args=None):
        logging.debug("{0}._handle_destroy({1}, {2})".format(self.__class__.__name__,
                                                             event_signal,
                                                             event_args
                                                             )
                      )
        pass

    def _handle_destroy_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_destroy_event({1}, {2})".format(self.__class__.__name__,
                                                                   event_signal,
                                                                   event_args
                                                                   )
                      )
        pass

    def _handle_direction_changed(self, event_signal, event_args=None):
        logging.debug("{0}._handle_direction_changed({1}, {2})".format(self.__class__.__name__,
                                                                       event_signal,
                                                                       event_args
                                                                       )
                      )
        pass

    def _handle_drag_begin(self, event_signal, event_args=None):
        logging.debug("{0}._handle_drag_begin({1}, {2})".format(self.__class__.__name__,
                                                                event_signal,
                                                                event_args
                                                                )
                      )
        pass

    def _handle_drag_data_delete(self, event_signal, event_args=None):
        logging.debug("{0}._handle_drag_data_delete({1}, {2})".format(self.__class__.__name__,
                                                                      event_signal,
                                                                      event_args
                                                                      )
                      )
        pass

    def _handle_drag_data_get(self, event_signal, event_args=None):
        logging.debug("{0}._handle_drag_data_get({1}, {2})".format(self.__class__.__name__,
                                                                   event_signal,
                                                                   event_args
                                                                   )
                      )
        pass

    def _handle_drag_data_received(self, event_signal, event_args=None):
        logging.debug("{0}._handle_drag_data_received({1}, {2})".format(self.__class__.__name__,
                                                                        event_signal,
                                                                        event_args
                                                                        )
                      )
        pass

    def _handle_drag_drop(self, event_signal, event_args=None):
        logging.debug("{0}._handle_drag_drop({1}, {2})".format(self.__class__.__name__,
                                                               event_signal,
                                                               event_args
                                                               )
                      )
        pass

    def _handle_drag_end(self, event_signal, event_args=None):
        logging.debug("{0}._handle_drag_end({1}, {2})".format(self.__class__.__name__,
                                                              event_signal,
                                                              event_args
                                                              )
                      )
        pass

    def _handle_drag_failed(self, event_signal, event_args=None):
        logging.debug("{0}._handle_drag_failed({1}, {2})".format(self.__class__.__name__,
                                                                 event_signal,
                                                                 event_args
                                                                 )
                      )
        pass

    def _handle_drag_leave(self, event_signal, event_args=None):
        logging.debug("{0}._handle_drag_leave({1}, {2})".format(self.__class__.__name__,
                                                                event_signal,
                                                                event_args
                                                                )
                      )
        pass

    def _handle_drag_motion(self, event_signal, event_args=None):
        logging.debug("{0}._handle_drag_motion({1}, {2})".format(self.__class__.__name__,
                                                                 event_signal,
                                                                 event_args
                                                                 )
                      )
        pass

    def _handle_draw(self, event_signal, event_args=None):
        logging.debug("{0}._handle_draw({1}, {2})".format(self.__class__.__name__,
                                                          event_signal,
                                                          event_args
                                                          )
                      )
        pass

    def _handle_enter_notify_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_enter_notify_event({1}, {2})".format(self.__class__.__name__,
                                                                        event_signal,
                                                                        event_args
                                                                        )
                      )
        pass

    def _handle_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_event({1}, {2})".format(self.__class__.__name__,
                                                           event_signal,
                                                           event_args
                                                           )
                      )
        pass

    def _handle_event_after(self, event_signal, event_args=None):
        logging.debug("{0}._handle_event_after({1}, {2})".format(self.__class__.__name__,
                                                                 event_signal,
                                                                 event_args
                                                                 )
                      )
        pass

    def _handle_focus(self, event_signal, event_args=None):
        logging.debug("{0}._handle_focus({1}, {2})".format(self.__class__.__name__,
                                                           event_signal,
                                                           event_args
                                                           )
                      )

        widget_to_set = GLXCurses.Application().get_widget_by_id(event_args["id"])

        if isinstance(widget_to_set, GLXCurses.Widget):

            for child in GLXCurses.Application().active_widgets:
                if hasattr(child.widget, 'has_focus'):
                    if child.id == widget_to_set.id:
                        child.widget.has_focus = True
                        GLXCurses.Application().has_focus = widget_to_set
                    else:
                        child.widget.has_focus = False

    def _handle_focus_in_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_focus_in_event({1}, {2})".format(self.__class__.__name__,
                                                                    event_signal,
                                                                    event_args
                                                                    )
                      )
        pass

    def _handle_focus_out_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_focus_out_event({1}, {2})".format(self.__class__.__name__,
                                                                     event_signal,
                                                                     event_args
                                                                     )
                      )
        pass

    def _handle_grab_broken_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_grab_broken_event({1}, {2})".format(self.__class__.__name__,
                                                                       event_signal,
                                                                       event_args
                                                                       )
                      )
        pass

    def _handle_grab_focus(self, event_signal, event_args=None):
        logging.debug("{0}._handle_grab_focus({1}, {2})".format(self.__class__.__name__,
                                                                event_signal,
                                                                event_args
                                                                )
                      )

        widget_to_set = GLXCurses.Application().get_widget_by_id(event_args["id"])

        if isinstance(widget_to_set, GLXCurses.Widget):

            for child in GLXCurses.Application().active_widgets:
                if hasattr(child.widget, 'has_focus'):
                    if child.id == widget_to_set.id:
                        child.widget.has_focus = True
                        GLXCurses.Application().has_focus = widget_to_set
                    else:
                        child.widget.has_focus = False

                if hasattr(child.widget, 'has_default'):
                    if child.id == widget_to_set.id:
                        child.widget.has_default = True
                        GLXCurses.Application().has_default = widget_to_set
                    else:
                        child.widget.has_default = False

                if hasattr(child.widget, 'has_prelight'):
                    if child.id == widget_to_set.id:
                        child.widget.has_prelight = True
                        GLXCurses.Application().has_prelight = widget_to_set
                    else:
                        child.widget.has_prelight = False

    def _handle_grab_notify(self, event_signal, event_args=None):
        logging.debug("{0}._handle_grab_notify({1}, {2})".format(self.__class__.__name__,
                                                                 event_signal,
                                                                 event_args
                                                                 )
                      )
        pass

    def _handle_hide(self, event_signal, event_args=None):
        logging.debug("{0}._handle_hide({1}, {2})".format(self.__class__.__name__,
                                                          event_signal,
                                                          event_args
                                                          )
                      )
        pass

    def _handle_hierarchy_changed(self, event_signal, event_args=None):
        logging.debug("{0}._handle_hierarchy_changed({1}, {2})".format(self.__class__.__name__,
                                                                       event_signal,
                                                                       event_args
                                                                       )
                      )
        pass

    def _handle_key_press_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_key_press_event({1}, {2})".format(self.__class__.__name__,
                                                                     event_signal,
                                                                     event_args
                                                                     )
                      )
        pass

    def _handle_key_release_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_key_release_event({1}, {2})".format(self.__class__.__name__,
                                                                       event_signal,
                                                                       event_args
                                                                       )
                      )
        pass

    def _handle_keynav_failed(self, event_signal, event_args=None):
        logging.debug("{0}._handle_keynav_failed({1}, {2})".format(self.__class__.__name__,
                                                                   event_signal,
                                                                   event_args
                                                                   )
                      )
        pass

    def _handle_leave_notify_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_leave_notify_event({1}, {2})".format(self.__class__.__name__,
                                                                        event_signal,
                                                                        event_args
                                                                        )
                      )
        pass

    def _handle_map(self, event_signal, event_args=None):
        logging.debug("{0}._handle_map({1}, {2})".format(self.__class__.__name__,
                                                         event_signal,
                                                         event_args
                                                         )
                      )
        pass

    def _handle_map_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_map_event({1}, {2})".format(self.__class__.__name__,
                                                               event_signal,
                                                               event_args
                                                               )
                      )
        pass

    def _handle_mnemonic_activate(self, event_signal, event_args=None):
        logging.debug("{0}._handle_mnemonic_activate({1}, {2})".format(self.__class__.__name__,
                                                                       event_signal,
                                                                       event_args
                                                                       )
                      )
        pass

    def _handle_motion_notify_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_motion_notify_event({1}, {2})".format(self.__class__.__name__,
                                                                         event_signal,
                                                                         event_args
                                                                         )
                      )
        pass

    def _handle_move_focus(self, event_signal, event_args=None):
        logging.debug("{0}._handle_move_focus({1}, {2})".format(self.__class__.__name__,
                                                                event_signal,
                                                                event_args
                                                                )
                      )
        pass

    def _handle_parent_set(self, event_signal, event_args=None):
        logging.debug("{0}._handle_parent_set({1}, {2})".format(self.__class__.__name__,
                                                                event_signal,
                                                                event_args
                                                                )
                      )
        pass

    def _handle_popup_menu(self, event_signal, event_args=None):
        logging.debug("{0}._handle_popup_menu({1}, {2})".format(self.__class__.__name__,
                                                                event_signal,
                                                                event_args
                                                                )
                      )
        pass

    def _handle_property_notify_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_property_notify_event({1}, {2})".format(self.__class__.__name__,
                                                                           event_signal,
                                                                           event_args
                                                                           )
                      )
        pass

    def _handle_proximity_in_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_proximity_in_event({1}, {2})".format(self.__class__.__name__,
                                                                        event_signal,
                                                                        event_args
                                                                        )
                      )
        pass

    def _handle_proximity_out_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_proximity_out_event({1}, {2})".format(self.__class__.__name__,
                                                                         event_signal,
                                                                         event_args
                                                                         )
                      )
        pass

    def _handle_query_tooltip(self, event_signal, event_args=None):
        logging.debug("{0}._handle_query_tooltip({1}, {2})".format(self.__class__.__name__,
                                                                   event_signal,
                                                                   event_args
                                                                   )
                      )
        pass

    def _handle_realize(self, event_signal, event_args=None):
        logging.debug("{0}._handle_realize({1}, {2})".format(self.__class__.__name__,
                                                             event_signal,
                                                             event_args
                                                             )
                      )
        pass

    def _handle_screen_changed(self, event_signal, event_args=None):
        logging.debug("{0}._handle_screen_changed({1}, {2})".format(self.__class__.__name__,
                                                                    event_signal,
                                                                    event_args
                                                                    )
                      )
        pass

    def _handle_scroll_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_scroll_event({1}, {2})".format(self.__class__.__name__,
                                                                  event_signal,
                                                                  event_args
                                                                  )
                      )
        pass

    def _handle_selection_clear_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_selection_clear_event({1}, {2})".format(self.__class__.__name__,
                                                                           event_signal,
                                                                           event_args
                                                                           )
                      )
        pass

    def _handle_selection_get(self, event_signal, event_args=None):
        logging.debug("{0}._handle_selection_get({1}, {2})".format(self.__class__.__name__,
                                                                   event_signal,
                                                                   event_args
                                                                   )
                      )
        pass

    def _handle_selection_notify_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_selection_notify_event({1}, {2})".format(self.__class__.__name__,
                                                                            event_signal,
                                                                            event_args
                                                                            )
                      )
        pass

    def _handle_selection_received(self, event_signal, event_args=None):
        logging.debug("{0}._handle_selection_received({1}, {2})".format(self.__class__.__name__,
                                                                        event_signal,
                                                                        event_args
                                                                        )
                      )
        pass

    def _handle_selection_request_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_selection_request_event({1}, {2})".format(self.__class__.__name__,
                                                                             event_signal,
                                                                             event_args
                                                                             )
                      )
        pass

    def _handle_show(self, event_signal, event_args=None):
        logging.debug("{0}._handle_show({1}, {2})".format(self.__class__.__name__,
                                                          event_signal,
                                                          event_args
                                                          )
                      )
        pass

    def _handle_show_help(self, event_signal, event_args=None):
        logging.debug("{0}._handle_show_help({1}, {2})".format(self.__class__.__name__,
                                                               event_signal,
                                                               event_args
                                                               )
                      )
        pass

    def _handle_size_allocate(self, event_signal, event_args=None):
        logging.debug("{0}._handle_size_allocate({1}, {2})".format(self.__class__.__name__,
                                                                   event_signal,
                                                                   event_args
                                                                   )
                      )
        pass

    def _handle_state_changed(self, event_signal, event_args=None):
        logging.debug("{0}._handle_state_changed({1}, {2})".format(self.__class__.__name__,
                                                                   event_signal,
                                                                   event_args
                                                                   )
                      )
        pass

    def _handle_state_flags_changed(self, event_signal, event_args=None):
        logging.debug("{0}._handle_state_flags_changed({1}, {2})".format(self.__class__.__name__,
                                                                         event_signal,
                                                                         event_args
                                                                         )
                      )
        pass

    def _handle_style_set(self, event_signal, event_args=None):
        logging.debug("{0}._handle_style_set({1}, {2})".format(self.__class__.__name__,
                                                               event_signal,
                                                               event_args
                                                               )
                      )
        pass

    def _handle_style_updated(self, event_signal, event_args=None):
        logging.debug("{0}._handle_style_updated({1}, {2})".format(self.__class__.__name__,
                                                                   event_signal,
                                                                   event_args
                                                                   )
                      )
        pass

    def _handle_touch_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_touch_event({1}, {2})".format(self.__class__.__name__,
                                                                 event_signal,
                                                                 event_args
                                                                 )
                      )
        pass

    def _handle_unmap(self, event_signal, event_args=None):
        logging.debug("{0}._handle_unmap({1}, {2})".format(self.__class__.__name__,
                                                           event_signal,
                                                           event_args
                                                           )
                      )
        pass

    def _handle_unmap_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_unmap_event({1}, {2})".format(self.__class__.__name__,
                                                                 event_signal,
                                                                 event_args
                                                                 )
                      )
        pass

    def _handle_unrealize(self, event_signal, event_args=None):
        logging.debug("{0}._handle_unrealize({1}, {2})".format(self.__class__.__name__,
                                                               event_signal,
                                                               event_args
                                                               )
                      )
        pass

    def _handle_visibility_notify_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_visibility_notify_event({1}, {2})".format(self.__class__.__name__,
                                                                             event_signal,
                                                                             event_args
                                                                             )
                      )
        pass

    def _handle_window_state_event(self, event_signal, event_args=None):
        logging.debug("{0}._handle_window_state_event({1}, {2})".format(self.__class__.__name__,
                                                                        event_signal,
                                                                        event_args
                                                                        )
                      )
        pass
