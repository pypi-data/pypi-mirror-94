#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
from GLXCurses.libs.Spot import Spot
from GLXCurses.libs.ApplicationHandlers import Handlers
from glxeveloop import Bus
import logging
import threading
import sys

lock = threading.Lock()


#  Why the locale mechanism fails
#    » export LC_CTYPE=my_country.UTF-8
#    » installed locale: vendor_country.utf8
#  • user has trouble to find a suitable locale on each machine
#    » if proper encoding is found, language/country may not match
#  • want to install fr_FR.UTF-8?  system admin doesn’t care!
#  • only some tools / terminals use system locale data
#    » esp. xterm maintains its own width data
#  • heterogeneous network: rlogin / telnet
#    » terminal and application run on different machines
#    » they see different system locale data
#    »  it is in principle not possible to make sure that the locale data
# you get from the system matches the behaviour of your terminal


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args)
        return cls.instance


# https://developer.gnome.org/gtk3/stable/GtkApplication.html

class Application(Bus, GLXCurses.Area, Spot, Handlers, metaclass=Singleton):
    """
    :Description:

    Create a Application singleton instance.

    That class have the role of a Controller and a NCurses Wrapper.

    It have particularity to not be a GLXCurses.Widget, then have a tonne of function for be a fake GLXCurses.Widget.

    From GLXCurses point of view everything start with it component. All widget will be display and store inside it
    component.
    """

    def __init__(self):
        Bus.__init__(self)
        GLXCurses.Area.__init__(self)
        GLXCurses.Spot.__init__(self)
        # Hidden vars
        self.__style = None
        self.__parent = None
        self.__active_window = None
        self.__app_menu = None
        self.__menubar = None
        self.__register_session = None
        self.__screensaver_active = None

        self.__active_window_id = None
        self.__children = None
        self.__statusbar = None
        self.__messagebar = None
        self.__toolbar = None

        self.screen = GLXCurses.Screen()
        self.stdscr = self.screen.stdscr
        self.style = GLXCurses.Style()

        # Store object
        self.children = None
        self.menubar = None
        self.main_window = None
        self.statusbar = None
        self.messagebar = None
        self.toolbar = None

        Handlers.__init__(self)

        # Store Variables
        self.id = GLXCurses.new_id()
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        # State
        self.connect("CLAIM_PRELIGHT", self.__class__._handle_claim_prelight)
        self.connect("CLAIM_DEFAULT", self.__class__._handle_claim_default)
        self.connect("RELEASE_PRELIGHT", self.__class__._handle_release_prelight)
        self.connect("RELEASE_DEFAULT", self.__class__._handle_release_default)

        # Button
        self.connect("activate", self.__class__._handle_activate)
        self.connect("clicked", self.__class__._handle_activate)

        # Containers
        self.connect("add", self.__class__._handle_add)
        self.connect("check-resize", self.__class__._handle_check_resize)
        self.connect("remove", self.__class__._handle_remove)
        self.connect("set-focus-child", self.__class__._handle_set_focus_child)

        # Editable
        self.connect("changed", self.__class__._handle_changed)
        self.connect("delete-text", self.__class__._handle_delete_text)
        self.connect("insert-text", self.__class__._handle_insert_text)

        # Label
        self.connect("activate-current-link", self.__class__._handle_activate_current_link)
        self.connect("activate-link", self.__class__._handle_activate_link)
        self.connect("copy-clipboard", self.__class__._handle_copy_clipboard)
        self.connect("move-cursor", self.__class__._handle_move_cursor)
        self.connect("populate-popup", self.__class__._handle_populate_popup)

        # TextView
        self.connect("backspace", self.__class__._handle_backspace)
        self.connect("copy-clipboard", self.__class__._handle_copy_clipboard)
        self.connect("cut-clipboard", self.__class__._handle_cut_clipboard)
        self.connect("delete-from-cursor", self.__class__._handle_delete_from_cursor)
        self.connect("extend-selection", self.__class__._handle_extend_selection)
        self.connect("insert-at-cursor", self.__class__._handle_insert_at_cursor)
        self.connect("insert-emoji", self.__class__._handle_insert_emoji)
        self.connect("move-cursor", self.__class__._handle_move_cursor)
        self.connect("move-viewport", self.__class__._handle_move_viewport)
        self.connect("paste-clipboard", self.__class__._handle_paste_clipboard)
        self.connect("populate-popup", self.__class__._handle_populate_popup)
        self.connect("preedit-changed", self.__class__._handle_preedit_changed)
        self.connect("select-all", self.__class__._handle_select_all)
        self.connect("set-anchor", self.__class__._handle_set_anchor)
        self.connect("toggle-cursor-visible", self.__class__._handle_toggle_cursor_visible)
        self.connect("toggle-overwrite", self.__class__._handle_toggle_overwrite)

        # Widget
        self.connect("accel-closures-changed", self.__class__._handle_accel_closures_changed)
        self.connect("button-press-event", self.__class__._handle_button_press_event)
        self.connect("button-release-event", self.__class__._handle_button_release_event)
        self.connect("can-activate-accel", self.__class__._handle_can_activate_accel)
        self.connect("child-notify", self.__class__._handle_child_notify)
        self.connect("composited-changed", self.__class__._handle_composited_changed)
        self.connect("configure-event", self.__class__._handle_configure_event)
        self.connect("damage-event", self.__class__._handle_damage_event)
        self.connect("delete-event", self.__class__._handle_delete_event)
        self.connect("destroy", self.__class__._handle_destroy)
        self.connect("destroy-event", self.__class__._handle_destroy_event)
        self.connect("direction-changed", self.__class__._handle_direction_changed)
        self.connect("drag-begin", self.__class__._handle_drag_begin)
        self.connect("drag-data-delete", self.__class__._handle_drag_data_delete)
        self.connect("drag-data-get", self.__class__._handle_drag_data_get)
        self.connect("drag-data-received", self.__class__._handle_drag_data_received)
        self.connect("drag-drop", self.__class__._handle_drag_drop)
        self.connect("drag-end", self.__class__._handle_drag_end)
        self.connect("drag-failed", self.__class__._handle_drag_failed)
        self.connect("drag-leave", self.__class__._handle_drag_leave)
        self.connect("drag-motion", self.__class__._handle_drag_motion)
        self.connect("draw", self.__class__._handle_draw)
        self.connect("enter-notify-event", self.__class__._handle_enter_notify_event)
        self.connect("event", self.__class__._handle_event)
        self.connect("event-after", self.__class__._handle_event_after)
        self.connect("focus", self.__class__._handle_focus)
        self.connect("focus-in-event", self.__class__._handle_focus_in_event)
        self.connect("focus-out-event", self.__class__._handle_focus_out_event)
        self.connect("grab-broken-event", self.__class__._handle_grab_broken_event)
        self.connect("grab-focus", self.__class__._handle_grab_focus)
        self.connect("grab-notify", self.__class__._handle_grab_notify)
        self.connect("hide", self.__class__._handle_hide)
        self.connect("hierarchy-changed", self.__class__._handle_hierarchy_changed)
        self.connect("key-press-event", self.__class__._handle_key_press_event)
        self.connect("key-release-event", self.__class__._handle_key_release_event)
        self.connect("keynav-failed", self.__class__._handle_keynav_failed)
        self.connect("leave-notify-event", self.__class__._handle_leave_notify_event)
        self.connect("map", self.__class__._handle_map)
        self.connect("map-event", self.__class__._handle_map_event)
        self.connect("mnemonic-activate", self.__class__._handle_mnemonic_activate)
        self.connect("motion-notify-event", self.__class__._handle_motion_notify_event)
        self.connect("move-focus", self.__class__._handle_move_focus)
        self.connect("parent-set", self.__class__._handle_parent_set)
        self.connect("popup-menu", self.__class__._handle_popup_menu)
        self.connect("property-notify-event", self.__class__._handle_property_notify_event)
        self.connect("proximity-in-event", self.__class__._handle_proximity_in_event)
        self.connect("proximity-out-event", self.__class__._handle_proximity_out_event)
        self.connect("query-tooltip", self.__class__._handle_query_tooltip)
        self.connect("realize", self.__class__._handle_realize)
        self.connect("screen-changed", self.__class__._handle_screen_changed)
        self.connect("scroll-event", self.__class__._handle_scroll_event)
        self.connect("selection-clear-event", self.__class__._handle_selection_clear_event)
        self.connect("selection-get", self.__class__._handle_selection_get)
        self.connect("selection-notify-event", self.__class__._handle_selection_notify_event)
        self.connect("selection-received", self.__class__._handle_selection_received)
        self.connect("selection-request-event", self.__class__._handle_selection_request_event)
        self.connect("show", self.__class__._handle_show)
        self.connect("show-help", self.__class__._handle_show_help)
        self.connect("size-allocate", self.__class__._handle_size_allocate)
        self.connect("state-changed", self.__class__._handle_state_changed)
        self.connect("state-flags-changed", self.__class__._handle_state_flags_changed)
        self.connect("style-set", self.__class__._handle_style_set)
        self.connect("style-updated", self.__class__._handle_style_updated)
        self.connect("touch-event", self.__class__._handle_touch_event)
        self.connect("unmap", self.__class__._handle_unmap)
        self.connect("unmap-event", self.__class__._handle_unmap_event)
        self.connect("unrealize", self.__class__._handle_unrealize)
        self.connect("visibility-notify-event", self.__class__._handle_visibility_notify_event)
        self.connect("window-state-event", self.__class__._handle_window_state_event)

    def _handle_claim_prelight(self, event_signal, event_args=None):
        logging.debug(
            "{0}._handle_claim_prelight({1}, {2})".format(
                self.__class__.__name__, event_signal, event_args
            )
        )
        widget_to_set = GLXCurses.Application().get_widget_by_id(event_args["id"])

        if isinstance(widget_to_set, GLXCurses.Widget):

            for child in GLXCurses.Application().active_widgets:
                if hasattr(child.widget, 'has_prelight'):
                    if child.id == widget_to_set.id:
                        child.widget.has_prelight = True
                        GLXCurses.Application().has_prelight = widget_to_set
                    else:
                        child.widget.has_prelight = False

    def _handle_claim_default(self, event_signal, event_args=None):
        logging.debug(
            "{0}._handle_claim_default({1}, {2})".format(
                self.__class__.__name__, event_signal, event_args
            )
        )
        widget_to_set = GLXCurses.Application().get_widget_by_id(event_args["id"])

        if isinstance(widget_to_set, GLXCurses.Widget):

            for child in GLXCurses.Application().active_widgets:
                if hasattr(child.widget, 'has_default'):
                    if child.id == widget_to_set.id:
                        child.widget.has_default = True
                        GLXCurses.Application().has_default = widget_to_set
                    else:
                        child.widget.has_default = False

    def _handle_release_default(self, event_signal, event_args=None):
        self.has_default = None

    def _handle_release_prelight(self, event_signal, event_args=None):
        self.has_prelight = None

    def get_widget_by_id(self, widget_id=None):
        if widget_id is None:
            raise TypeError\
                ("widget_id cannot be None")

        for widget in self.active_widgets:
            if widget.id == widget_id:
                return widget.widget

        raise ValueError("id {0} cannot be found in known widget.".format(widget_id))

    @property
    def active_window(self):
        """
        Gets the “active_window” for the application.

        The active :class:`Window <GLXCurses.Window.Window>` is the one that was most recently focused
        (within the application).

        This window may not have the focus at the moment if another application
        has it — this is just the most recently-focused window within this application.

        :return: the active :class:`Window <GLXCurses.Window.Window>`, or None if there isn't one.
        :rtype: GLXCurses.Window or None
        """
        windows_to_display = None
        for child in self.children:
            if child.id == self.active_window_id:
                windows_to_display = child

        # If a active window is found
        if windows_to_display is not None:
            return windows_to_display
        else:
            return None

    @active_window.setter
    def active_window(self, window=None):
        """
        Set the ``active_window`` property

        :param window: The window it be active in the Application
        :type window: GLXCurses.libs.ChildElement.ChildElement or None
        """
        if (
                window is not None and
                not hasattr(window, 'widget') and
                not isinstance(window.widget, GLXCurses.Window) and
                not isinstance(window.widget, GLXCurses.Dialog)
        ):
            raise TypeError('"active_window" must be a GLXCurses.Window , GLXCurses.Dialog or None')

        if window.id != self.active_window_id:
            self.active_window_id = window.id

    @property
    def children(self):
        """
        Store the ``children`` property value

        It property is use for store a stack of windows object use during choice of the active window

        Default value: []

        :return: ``children`` property value
        :rtype: list
        """
        return self.__children

    @children.setter
    def children(self, value=None):
        """
        Set the ``children`` property value

        Default value: []

        :param value:
        :type value: list or None
        """
        if value is None:
            value = []

        if type(value) != list:
            raise TypeError("'children' property value must be a list type or None")

        if self.children != value:
            self.__children = value

    @property
    def app_menu(self):
        return self.__app_menu

    @app_menu.setter
    def app_menu(self, app_menu=None):
        if not isinstance(app_menu, GLXCurses.MenuBar) and app_menu is not None:
            raise TypeError("'app_menu' must be a GLXCurses.MenuBar instance")
        if isinstance(app_menu, GLXCurses.MenuBar):
            app_menu.parent = self
        elif app_menu is None and isinstance(self.app_menu, GLXCurses.MenuBar):
            self.app_menu.parent = None
        if self.app_menu != app_menu:
            self.__app_menu = app_menu
            if self.app_menu:
                self.emit("add", {"widget": app_menu, "id": app_menu.id})

    @property
    def menubar(self):
        """
        The MenuModel for the menubar.

        :return: menubar property value
        :rtype: GLXCurses.MenuBar or None
        """
        return self.__menubar

    @menubar.setter
    def menubar(self, menubar=None):
        """
        menubar property

        :param menubar: a GLXCurses.MenuBar object or None for remove one.
        :type menubar: GLXCurses.MenuBar or None
        """
        if not isinstance(menubar, GLXCurses.MenuBar) and menubar is not None:
            raise TypeError("'menubar' must be a GLXCurses.MenuBar instance")
        if isinstance(menubar, GLXCurses.MenuBar):
            menubar.parent = self
        elif menubar is None and isinstance(self.menubar, GLXCurses.MenuBar):
            self.menubar.parent = None
        if menubar is None:
            self.__menubar = None
            return
        if self.menubar != menubar:
            self.__menubar = menubar
            if self.menubar:
                self.emit("add", {"widget": menubar, "id": menubar.id})

    @property
    def register_session(self):
        return self.__register_session

    @register_session.setter
    def register_session(self, register_session=None):
        if self.register_session != register_session:
            self.__register_session = register_session

    @property
    def screensaver_active(self):
        return self.__screensaver_active

    @screensaver_active.setter
    def screensaver_active(self, screensaver_active=None):
        if self.screensaver_active != screensaver_active:
            self.__screensaver_active = screensaver_active

    # internal property
    @property
    def style(self):
        """
        The style of the Application, which contains information about how it will look (colors, etc).

        The Application Style is impose to each widget

        :return: a GLXCurses.Style instance
        :rtype: GLXCurses.Style
        """
        return self.__style

    @style.setter
    def style(self, style=None):
        """
        Set the ``style`` property.

        :param style: a GLXCurses.Style instance
        :type style: GLXCurses.Style
        :raise TypeError: When style is not a GLXCurses.Style instance or None
        """
        if style is None:
            style = GLXCurses.Style()
        if not isinstance(style, GLXCurses.Style):
            raise TypeError('"style" must be a GLXCurses.Style instance or None')
        if self.style != style:
            self.__style = style

    @property
    def statusbar(self):
        return self.__statusbar

    @statusbar.setter
    def statusbar(self, statusbar=None):
        if statusbar is not None and not isinstance(statusbar, GLXCurses.StatusBar):
            raise TypeError('"statusbar" must be a StatusBar instance or None')
        if statusbar is None:
            self.__statusbar = None
            return
        if self.statusbar != statusbar:
            self.__statusbar = statusbar
            # EVENT EMIT
            self.emit("add", {"widget": statusbar, "id": statusbar.id})
            if isinstance(self.statusbar, GLXCurses.StatusBar):
                self.statusbar.parent = self

    @property
    def messagebar(self):
        """
        Sets the messagebar of application .

        This can only be done in the primary instance of the application, after it has been registered.
        “startup” is a good place to call this.

        :return: the ``messagebar`` property value
        :rtype: GLXCurses.MessageBar or None
        """
        return self.__messagebar

    @messagebar.setter
    def messagebar(self, messagebar=None):
        """
        Set the ``messagebar`` property value

        :param messagebar: a :class:`MessageBar <GLXCurses.MessageBar.MessageBar>`
        :type messagebar: GLXCurses.MessageBar
        :raise TypeError: if ``messagebar`` parameter is not a MessageBar type or None
        """
        if messagebar is not None and not isinstance(messagebar, GLXCurses.MessageBar):
            raise TypeError('"messagebar" must be a MessageBar instance or None')
        if messagebar is None:
            self.__messagebar = None
            return
        if self.messagebar != messagebar:
            self.__messagebar = messagebar
            # EVENT EMIT
            self.emit("add", {"widget": messagebar, "id": messagebar.id})
            if isinstance(self.messagebar, GLXCurses.MessageBar):
                self.messagebar.parent = self

    @property
    def toolbar(self):
        return self.__toolbar

    @toolbar.setter
    def toolbar(self, toolbar=None):
        if toolbar is not None and not isinstance(toolbar, GLXCurses.ToolBar):
            raise TypeError('"toolbar" must be a ToolBar instance or None')
        if toolbar is None:
            self.__toolbar = None
            return
        if self.toolbar != toolbar:
            self.__toolbar = toolbar
            self.emit("add", {"widget": toolbar, "id": toolbar.id})

    # GLXCApplication function
    # Re Order
    def add_window(self, window):
        """
        Add a :class:`Window <GLXCurses.Window.Window>` widget to the\
        :class:`Application <GLXCurses.Application.Application>` windows children's list.

        This call can only happen after the application has started; typically, you should add new application windows
        in response to the emission of the “activate” signal.

        This call is equivalent to setting the “application” property of window to application .

        Normally, the connection between the application and the window will remain until the window is destroyed,
        but you can explicitly remove it with application.remove_window().

        Galaxie-Curses will keep the application running as long as it has any windows.

        :param window: a window to add
        :type window: GLXCurses.Window
        :raise TypeError: if ``window`` parameter is not a :class:`Window <GLXCurses.Window.Window>` type
        """
        # Exit as soon of possible
        # Check if window is a Galaxie Window
        if not isinstance(window, GLXCurses.Window):
            raise TypeError("'window' must be a GLXCurses.Window instance")

        # set application
        window.application = self
        # set the Application it self as parent of the child window
        window.parent = self
        window.stdscr = self.stdscr

        # create a dictionary structure for add it to windows list
        child_to_add = GLXCurses.ChildElement(
            widget_name=window.name,
            widget_id=window.id,
            widget=window,
            widget_type=window.glxc_type,
        )
        if child_to_add not in self.children:
            self.children.append(child_to_add)
            self.emit("add", {"widget": child_to_add.widget, "id": child_to_add.id})

        # Make the last added element active
        if self.active_window != self.children[-1]:
            self.active_window = self.children[-1]

    def remove_window(self, window):
        """
        Remove a :class:`Window <GLXCurses.Window.Window>` widget from the\
        :class:`Application <GLXCurses.Application.Application>` windows children's list.

        Set"application" and "parent' attribute of the :func:`GLXCurses.Window <GLXCurses.Window.Window>`
        to :py:obj:`None`.

        :param window: a window to add
        :type window: GLXCurses.Window
        :raise TypeError: if ``window`` parameter is not a :class:`Window <GLXCurses.Window.Window>` type
        """
        # Exit as soon of possible
        # Check if window is a Galaxie Window
        if not isinstance(window, GLXCurses.Window):
            raise TypeError("'window' must be a GLXCurses.Window instance")

        # Detach the children
        window.parent = None
        window.application = None

        # Search for the good window id and delete it from the window list
        count = 0
        last_found = None
        for child in self.children:
            if child.id == window.id:
                last_found = count
            count += 1

        if last_found is not None:
            self.children.pop(last_found)
            if len(self.children) - 1 >= 0:
                self.active_window = self.children[-1]

    def get_window_by_id(self, identifier=None):
        """
        Returns the GtkApplicationWindow with the given ID.

        :param identifier: an identifier number
        :type identifier: int
        :return: the window with ID ``identifier`` , or None if there is no window with this ID.
        :rtype: int or None
        :raise TypeError: when ``identifier`` is nt a int type
        """
        if not GLXCurses.is_valid_id(identifier):
            raise TypeError('"identifier" must be a int type')
        for child in self.children:
            if child.id == identifier:
                return child
        return None

    def refresh(self):
        """
        Refresh the NCurses Screen, and redraw each contain widget's

        It's a central refresh point for the entire application.
        """
        self.screen.touch_screen()

        self.check_sizes()

        if self.height > 0 and self.active_window:
            if (
                    isinstance(self.active_window.widget, GLXCurses.Dialog)
                    or Application().has_focus is not None
                    and isinstance(Application().has_focus.widget, GLXCurses.Menu)
            ):
                prev_child = None
                for child in self.children:
                    if child.id == GLXCurses.Application().active_window_id_prev:
                        prev_child = child

                if prev_child:
                    prev_child.widget.x = self.x
                    prev_child.widget.y = self.y
                    prev_child.widget.width = self.width
                    prev_child.widget.height = self.height
                    prev_child.widget.draw()

        if self.active_window:
            self.active_window.widget.draw()

        if self.messagebar:
            self.messagebar.draw()

        if self.statusbar:
            self.statusbar.draw()

        if self.menubar:
            self.menubar.draw()

        if self.toolbar:
            self.toolbar.draw()

        self.screen.refresh()

    def check_sizes(self):
        """
        Just a internal method for compute every size.

        It consist to a serial of testable function call
        """
        # Get stdscr information
        screen_y, screen_x = self.stdscr.getbegyx()
        screen_height, screen_width = self.stdscr.getmaxyx()

        if self.menubar:
            self.menubar.stdscr = self.stdscr
            self.menubar.y = screen_y
            self.menubar.x = screen_x
            self.menubar.width = screen_width
            self.menubar.height = 1

        if self.messagebar:
            self.messagebar.stdscr = self.stdscr
            self.messagebar.y = (
                    screen_height
                    - 1
                    - (int(bool(self.statusbar)) + int(bool(self.toolbar)))
            )
            self.messagebar.x = screen_x
            self.messagebar.width = screen_width
            self.messagebar.height = 1

        if self.statusbar:
            self.statusbar.stdscr = self.stdscr
            self.statusbar.y = screen_height - 1 - int(bool(self.toolbar))
            self.statusbar.x = screen_x
            self.statusbar.width = screen_width
            self.statusbar.height = 1

        if self.toolbar:
            self.toolbar.stdscr = self.stdscr
            self.toolbar.y = screen_height - 1
            self.toolbar.x = screen_x
            self.toolbar.width = screen_width
            self.toolbar.height = 1

        # Area of Application is a zone where the active Windows will have it sizes impose by it.
        self.height = screen_height - (
                int(bool(self.menubar))
                + int(bool(self.messagebar))
                + int(bool(self.statusbar))
                + int(bool(self.toolbar))
        )
        self.width = screen_width
        self.x = 0
        self.y = int(bool(self.menubar))

        # If we have a active windows, (must be a Container for true, but we impose a Window with add_window())
        if self.active_window:
            # Dialog use screen location
            if isinstance(self.active_window.widget, GLXCurses.Dialog):
                self.active_window.widget.stdscr = self.stdscr
                self.active_window.widget.x = screen_x
                self.active_window.widget.y = screen_y
                self.active_window.widget.width = screen_width
                self.active_window.widget.height = screen_height
            else:
                # Impose the Window area setting, it can be use like that by all Widget inside the Window container
                # that the role of teh container to impose it Area size to every children. Here that is the root of
                # the area
                self.active_window.widget.stdscr = self.stdscr
                self.active_window.widget.style = self.style
                self.active_window.widget.y = self.y
                self.active_window.widget.x = self.x
                self.active_window.widget.width = self.width
                self.active_window.widget.height = self.height

    # Galaxie EvLoop

    def get_mouse(self):
        return self.screen.get_mouse()

    def eveloop_input_event(self):
        event = self.screen.lowlevel_getch()
        if event != -1:
            # curses.mouse event
            if event == 409:
                # get mouse position from GLXCurses.Application() class
                self.emit("MOUSE_EVENT", self.get_mouse())
            # curses event
            else:
                self.emit("CURSES", event)

    def eveloop_cmd(self):
        self.refresh()

    def eveloop_finalization(self):
        self.screen.close()

    def eveloop_dispatch_application(self, detailed_signal, args):
        """
        Flush Mainloop event to Child's father's for a Widget's recursive event dispatch

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param args: additional parameters arg1, arg2
        :type args: list
        """
        self.events_flush(detailed_signal, args)
        if (
                self.menubar and
                hasattr(self.menubar, 'events_dispatch') and
                self.has_focus and
                hasattr(self.has_focus, 'widget') and
                self.menubar == self.has_focus.widget
        ):
            self.menubar.events_dispatch(
                detailed_signal,
                args
            )

        else:
            if self.active_window and hasattr(self.active_window, 'widget'):
                self.active_window.widget.events_dispatch(
                    detailed_signal,
                    args
                )

        if not isinstance(self.active_window.widget, GLXCurses.Dialog):
            if self.menubar and hasattr(self.menubar, 'events_dispatch'):
                self.menubar.events_dispatch(
                    detailed_signal,
                    args
                )
            if self.toolbar and hasattr(self.toolbar, 'events_dispatch'):
                self.toolbar.events_dispatch(
                    detailed_signal,
                    args
                )

    def eveloop_keyboard_interruption(self):
        if self.permit_keyboard_interruption:
            GLXCurses.mainloop.stop()
        else:
            # Ctrl + C
            self.emit("CURSES", 3)
