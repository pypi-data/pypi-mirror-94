#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

# Inspired from: https://developer.gnome.org/gtk3/stable/GtkStyle.html

import GLXCurses


class Style(GLXCurses.Colors):
    """
    :Description:

    Galaxie Curses Style is equivalent to a skin feature, the entire API receive a common Style from Application
    and each individual Widget can use it own separate one.

    Yet it's a bit hard to explain how create you own Style, in summary it consist to a dict() it have keys
    with a special name call ``Attribute``, inside that dictionary we create a second level of dict() dedicated
    to store color value of each ``States``
    """

    def __init__(self):
        GLXCurses.Colors.__init__(self)
        """
        :GLXCurses Style Attributes Type:

         +-------------+---------------------------------------------------------------------------------------------+
         | ``text_fg`` | An color to be used for the foreground colors in each curses_subwin state.                  |
         +-------------+---------------------------------------------------------------------------------------------+
         | ``bg``      | An color to be used for the background colors in each curses_subwin state.                  |
         +-------------+---------------------------------------------------------------------------------------------+
         | ``light``   | An color to be used for the light colors in each curses_subwin state.                       |
         +-------------+---------------------------------------------------------------------------------------------+
         | ``dark``    | An color to be used for the dark colors in each curses_subwin state.                        |
         +-------------+---------------------------------------------------------------------------------------------+
         | ``mid``     | An color to be used for the mid colors (between light and dark) in each curses_subwin state |
         +-------------+---------------------------------------------------------------------------------------------+
         | ``text``    | An color to be used for the text colors in each curses_subwin state.                        |
         +-------------+---------------------------------------------------------------------------------------------+
         | ``base``    | An color to be used for the base colors in each curses_subwin state.                        |
         +-------------+---------------------------------------------------------------------------------------------+
         | ``black``   | Used for the black color.                                                                   |
         +-------------+---------------------------------------------------------------------------------------------+
         | ``white``   | Used for the white color.                                                                   |
         +-------------+---------------------------------------------------------------------------------------------+

        :GLXCurses States Type:

         +------------------------+----------------------------------------------------------------+
         | ``STATE_NORMAL``       | The state during normal operation                              |
         +------------------------+----------------------------------------------------------------+
         | ``STATE_ACTIVE``       | The curses_subwin is currently active, such as a button pushed |
         +------------------------+----------------------------------------------------------------+
         | ``STATE_PRELIGHT``     | The mouse pointer is over the curses_subwin                    |
         +------------------------+----------------------------------------------------------------+
         | ``STATE_SELECTED``     | The curses_subwin is selected                                  |
         +------------------------+----------------------------------------------------------------+
         | ``STATE_INSENSITIVE``  | The curses_subwin is disabled                                  |
         +------------------------+----------------------------------------------------------------+

        """
        # It's a GLXCurse Type
        self.glxc_type = "GLXCurses.Style"
        self.id = GLXCurses.new_id()
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        self.__attributes_states = None
        self.attributes_states = None

    @property
    def default_attributes_states(self):
        """
        Return a default style, that will be use by the entire GLXCurses API via the ``__attribute_states`` object. \
        every Widget's  will receive it style by default.

        :return: A Galaxie Curses Style dictionary
        :rtype: dict
        """
        return {
            # An color to be used for the base colors in each curses_subwin state.
            'base': {'STATE_ACTIVE': (255, 255, 255),
                     'STATE_INSENSITIVE': (255, 255, 255),
                     'STATE_NORMAL': (0, 0, 255),
                     'STATE_PRELIGHT': (0, 255, 255),
                     'STATE_SELECTED': (255, 255, 255)},
            # An color to be used for the background colors in each curses_subwin state.
            'bg': {'STATE_ACTIVE': (0, 0, 255),
                   'STATE_INSENSITIVE': (0, 0, 255),
                   'STATE_NORMAL': (0, 0, 255),
                   'STATE_PRELIGHT': (0, 255, 255),
                   'STATE_SELECTED': (0, 255, 255)},
            # Used for the black color.
            'black': {'STATE_ACTIVE': (0, 0, 0),
                      'STATE_INSENSITIVE': (0, 0, 0),
                      'STATE_NORMAL': (0, 0, 0),
                      'STATE_PRELIGHT': (0, 0, 0),
                      'STATE_SELECTED': (0, 0, 0)},
            # An color to be used for the dark colors in each curses_subwin state.
            # The dark colors are slightly darker than the bg colors and used for creating shadows.
            'dark': {'STATE_ACTIVE': (0, 0, 0),
                     'STATE_INSENSITIVE': (0, 0, 0),
                     'STATE_NORMAL': (0, 0, 0),
                     'STATE_PRELIGHT': (0, 0, 0),
                     'STATE_SELECTED': (0, 0, 0)},
            # An color to be used for the light colors in each curses_subwin state.
            # The light colors are slightly lighter than the bg colors and used for creating shadows.
            'light': {'STATE_ACTIVE': (255, 255, 255),
                      'STATE_INSENSITIVE': (255, 255, 255),
                      'STATE_NORMAL': (0, 255, 255),
                      'STATE_PRELIGHT': (255, 255, 255),
                      'STATE_SELECTED': (255, 255, 255)},
            # An color to be used for the mid colors (between light and dark) in each curses_subwin state
            'mid': {'STATE_ACTIVE': (255, 255, 255),
                    'STATE_INSENSITIVE': (255, 255, 255),
                    'STATE_NORMAL': (255, 255, 0),
                    'STATE_PRELIGHT': (255, 255, 255),
                    'STATE_SELECTED': (255, 255, 255)},
            # An color to be used for the text colors in each curses_subwin state.
            'text': {'STATE_ACTIVE': (255, 255, 255),
                     'STATE_INSENSITIVE': (255, 255, 255),
                     'STATE_NORMAL': (180, 180, 180),
                     'STATE_PRELIGHT': (0, 0, 0),
                     'STATE_SELECTED': (255, 255, 255)},
            # An color to be used for the foreground colors in each curses_subwin state.
            'text_fg': {'STATE_ACTIVE': (255, 255, 255),
                        'STATE_INSENSITIVE': (255, 255, 255),
                        'STATE_NORMAL': (255, 255, 255),
                        'STATE_PRELIGHT': (255, 255, 255),
                        'STATE_SELECTED': (0, 0, 255)},
            # Used for the white color.
            'white': {'STATE_ACTIVE': (255, 255, 255),
                      'STATE_INSENSITIVE': (255, 255, 255),
                      'STATE_NORMAL': (255, 255, 255),
                      'STATE_PRELIGHT': (255, 255, 255),
                      'STATE_SELECTED': (255, 255, 255)}
        }

    @property
    def attributes_states(self):
        """
        Return the ``__attribute_states`` attribute, it consist to a dictionary it store a second level of dictionary \
        with keys if have special name.

        :return: attribute states dictionary on Galaxie Curses Style format
        :rtype: dict
        """
        return self.__attributes_states

    @attributes_states.setter
    def attributes_states(self, attributes_states=None):
        """
        Set the ``__attribute_states`` attribute, it consist to a dictionary it store a second level of dictionary \
        with keys if have special name.

        see: get_default_attribute_states() for generate a default Style.

        :param attributes_states: a Dictionary with Galaxie Curses Style format
        :type attributes_states: dict(dict(str()))
        """
        # Try to found a way to not be execute
        # Check first level dictionary
        if attributes_states is None:
            attributes_states = self.default_attributes_states

        if type(attributes_states) != dict:
            raise TypeError('"__attribute_states" is not a dictionary')

        # For each key's
        for attribute in [
            "text_fg",
            "bg",
            "light",
            "dark",
            "mid",
            "text",
            "base",
            "black",
            "white",
        ]:
            # Check if the key value is a dictionary
            try:
                if type(attributes_states[attribute]) != dict:
                    raise TypeError('"attribute_states" key is not a dict')
            except KeyError:
                raise KeyError('"attribute_states" is not a Galaxie Curses Style')
            # For each key value, in that case a sub dictionary
            for state in [
                "STATE_NORMAL",
                "STATE_ACTIVE",
                "STATE_PRELIGHT",
                "STATE_SELECTED",
                "STATE_INSENSITIVE",
            ]:
                # Check if the key value is a string
                try:
                    if type(attributes_states[attribute][state]) != tuple:
                        raise TypeError('"__attribute_states" key is not a tuple')
                except KeyError:
                    raise KeyError('"__attribute_states" is not a Galaxie Curses Style')

        # If it haven't quit that ok
        if attributes_states != self.attributes_states:
            self.__attributes_states = attributes_states

    def attribute_to_rgb(self, attribute="base", state="STATE_NORMAL"):
        """
        Return a text color, for a attribute and a state passed as argument, it's use by widget for know which color
        use, when a state change.

        By example: When color change if the button is pressed

        :param attribute: accepted value: text_fg
        :param state: accepted value: STATE_NORMAL, STATE_ACTIVE, STATE_PRELIGHT, STATE_SELECTED, STATE_INSENSITIVE
        :return: text color
        :rtype: str
        """
        return self.attributes_states[attribute][state]
