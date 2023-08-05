#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved


class Actionable(object):
    """
    Actionable — An interface for widgets that can be associated with actions

    **Known Implementations**
        Actionable is implemented by GLXC.Actionable and contain a list of widget
           Button,
           CheckButton,
           CheckMenuItem,
           ColorButton,
           FontButton,
           ImageMenuItem,
           LinkButton,
           ListBoxRow,
           LockButton,
           MenuButton,
           MenuItem,
           MenuToolButton,
           ModelButton,
           RadioButton,
           RadioMenuItem,
           RadioToolButton,
           ScaleButton,
           SeparatorMenuItem,
           Switch,
           TearoffMenuItem,
           ToggleButton,
           ToggleToolButton,
           ToolButton,
           VolumeButton.
    """

    def __init__(self):
        self.__action_name = None
        self.__action_target = None
        self.action_name = None
        self.action_target = None

    @property
    def action_name(self):
        return self.__action_name

    @action_name.setter
    def action_name(self, value=None):
        if value is not None and type(value) != str:
            raise TypeError("'action_name' must be a str type or None")
        if self.action_name != value:
            self.__action_name = value

    @property
    def action_target(self):
        return self.__action_target

    @action_target.setter
    def action_target(self, value=None):
        if self.action_target != value:
            self.__action_target = value

    def get_action_name(self):
        """
        Gets the action name for ``actionable`` .

        See set_action_name() for more information.

        :return: the action name, or None if unset.
        :rtype: str or None
        """
        return self.action_name

    def set_action_name(self, action_name=None):
        """
        Specifies the name of the action with which this widget should be associated.
        If action_name is NULL then the widget will be unassociated from any previous action.

        Usually this function is used when the widget is located (or will be located) within the hierarchy of a
        ApplicationWindow.

        Names are of the form “win.save” or “app.quit” for actions on the containing ApplicationWindow or
        its associated GLXCurses.Application, respectively.

        This is the same form used for actions in the GMenu associated with the window.

        :param action_name: an action name, or None.
        :type action_name: str or None
        :raise TypeError: if ``action_name`` is not a str type or None
        """
        self.action_name = action_name

    def get_action_target_value(self):
        """
        Gets the current target value of actionable .

        See gtk_actionable_set_action_target_value() for more information.

        :return: the current target value.
        :rtype: GLXCurses.Object or None
        """

        return self.action_target

    def set_action_target_value(self, target_value=None):
        """
        Gets the current target value of actionable .

        See gtk_actionable_set_action_target_value() for more information.

        :param target_value: the target value, or NULL
        :type target_value: GLXCurses.Object or None
        """
        self.action_target = target_value
