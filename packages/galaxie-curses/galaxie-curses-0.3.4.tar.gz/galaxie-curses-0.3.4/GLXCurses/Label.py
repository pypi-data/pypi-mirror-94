#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import textwrap
import logging


class Label(GLXCurses.Misc, GLXCurses.Movable):
    def __init__(self):
        # Load heritage
        GLXCurses.Misc.__init__(self)
        GLXCurses.Movable.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = "GLXCurses.Label"
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        # Label Properties
        self.__angle = None
        self.angle = None

        self.__attributes = None
        self.attributes = None

        self.__cursor_position = None
        self.cursor_position = None

        self.justify = GLXCurses.GLXC.JUSTIFY_LEFT

        self.__label = None
        self.label = None

        self.__lines = None
        self.lines = None

        self.__max_width_chars = None
        self.max_width_chars = None

        self.__mnemonic_keyval = None
        self.mnemonic_keyval = None

        self.__mnemonic_widget = None
        self.mnemonic_widget = None

        self.__pattern = None
        self.pattern = None

        self.__selectable = False
        self.selectable = False

        self.__selection_bound = None
        self.selection_bound = None

        self.__single_line_mode = None
        self.single_line_mode = None

        self.__track_visited_links = None
        self.track_visited_links = None

        self.__use_markdown = None
        self.use_markdown = None

        self.__use_underline = None
        self.use_underline = None

        self.__width_chars = None
        self.width_chars = None

        self.__wrap = None
        self.wrap = None

        self.__wrap_mode = None
        self.wrap_mode = GLXCurses.GLXC.WRAP_WORD

        self.text_x = 0
        self.text_y = 0

    ##############
    # Properties #
    ##############
    @property
    def angle(self):
        """
        The angle that the baseline of the label makes with the horizontal, in degrees, measured counterclockwise.
        An angle of 90 reads from from bottom to top, an angle of 270, from top to bottom.

        Ignored if the label is selectable.

        Allowed values: [0,360]

        :return: angle that the baseline of the label
        :rtype: int
        """
        return self.__angle

    @angle.setter
    def angle(self, angle=None):
        """
        Set the ``angle`` property value

        :param angle: The angle that the baseline of the label makes with the horizontal
        :type angle: int [0,360]
        :raise TypeError: When ``angle`` property value is not int type or None
        :raise ValueError: When ``angle`` property value is in allowed range [0,360]
        """
        if angle is None:
            angle = 0
        if type(angle) != int:
            raise TypeError("'angle' value must be a int type or None")
        if angle < 0 or angle > 360:
            raise ValueError("'angle' allowed value is [0,360]")
        if self.angle != angle:
            self.__angle = angle

    @property
    def attributes(self):
        """
        A list of style attributes to apply to the text of the label.

        :return: A list of style attributes
        :rtype: list
        """
        return self.__attributes

    @attributes.setter
    def attributes(self, attributes=None):
        """
        Set the ``attributes`` property value

        :param attributes: A list of style attributes
        :type attributes: list
        :raise TypeError: When ``attribute`` property value is not a list type or None
        """
        if attributes is None:
            attributes = []
        if type(attributes) != list:
            raise TypeError("'attributes' property value must be a list type or None")
        if self.attributes != attributes:
            self.__attributes = attributes

    @property
    def cursor_position(self):
        """
        The current position of the insertion cursor in chars.

        :return: The ``cursor_position`` property value
        :rtype: int
        """
        return self.__cursor_position

    @cursor_position.setter
    def cursor_position(self, cursor_position=None):
        """
        Set the ``cursor_position`` property value

        :param cursor_position: The current position of the insertion cursor in chars
        :type cursor_position: int
        :raise TypeError: When ``cursor_position`` property value is not a int type or None
        :raise ValueError: When ``cursor_position`` property value is not > or = to zero
        """
        if cursor_position is None:
            cursor_position = 0
        if type(cursor_position) != int:
            raise TypeError("'cursor_position' property value must be int type or None")
        if cursor_position < 0:
            raise ValueError("'cursor_position' property value must be > or = to zero")
        if self.cursor_position != cursor_position:
            self.__cursor_position = cursor_position

    @property
    def label(self):
        """
        The contents of the label.

        If the string contains TXT MarkDown, you will have to set the ``use_markdown`` property to True in order for
        the label to display the MarkDown attributes.

        See also set_markdown() for a convenience function that sets both this property and the ``use_markdown``
        property at the same time.

        If the string contains underlines acting as mnemonics, you will have to set the ``use_underline`` property
        to True in order for the label to display them.

        :return: The content of the label
        :rtype: str
        """
        return self.__label

    @label.setter
    def label(self, label=None):
        """
        Set the ``label`` property value

        :param label: Contents of the label
        :type label: str or None
        :raise TypeError: When ``label`` property value is not str type or None
        """
        if label is None:
            label = ""
        if type(label) != str:
            raise TypeError('"label" must be a str type or None')
        if self.label != label:
            self.__label = label

    @property
    def lines(self):
        """
        The number of lines to which an ellipsized, wrapping label should be limited. This property has no effect if
        the label is not wrapping or ellipsized.

        Set this property to -1 if you don't want to limit the number of lines.

        :return: The number of lines to which an ellipsized
        :rtype: int
        """
        return self.__lines

    @lines.setter
    def lines(self, lines=None):
        """
        Set the ``lines`` property value

        :param lines: The number of lines to which an ellipsized
        :type lines: int
        :raise TypeError: When ``lines`` property is not a int type or None
        :raise ValueError: When ``lines`` property value is not >= to -1
        """
        if lines is None:
            lines = -1
        if type(lines) != int:
            raise TypeError("'lines' property value must be int type or None")
        if not lines >= -1:
            raise ValueError("'lines' property value must be >= to -1")
        if self.lines != lines:
            self.__lines = lines

    @property
    def max_width_chars(self):
        """
        The desired maximum width of the label, in characters.

        If this property is set to -1, the width will be calculated automatically.

        See the section on text layout for details of how ``width_chars`` and ``max_width_chars`` determine the width
        of ellipsized and wrapped labels.

        :return: Maximum width of the label, in characters
        :rtype: int
        """
        return self.__max_width_chars

    @max_width_chars.setter
    def max_width_chars(self, max_width_chars=None):
        """
        Set the ``max_width_chars`` property value

        :param max_width_chars: The desired maximum width of the label, in characters.
        :type max_width_chars: int
        :raise TypeError: When ``max_width_chars`` property is not a int type or None
        :raise ValueError: When ``max_width_chars`` property value is not >= to -1
        """
        if max_width_chars is None:
            max_width_chars = -1
        if type(max_width_chars) != int:
            raise TypeError("'max_width_chars' property value must be int type or None")
        if not max_width_chars >= -1:
            raise ValueError("'max_width_chars' property value must be >= to -1")
        if self.max_width_chars != max_width_chars:
            self.__max_width_chars = max_width_chars

    @property
    def mnemonic_keyval(self):
        """
        The mnemonic accelerator key for this label.

        Default value: 16777215
        """
        return self.__mnemonic_keyval

    @mnemonic_keyval.setter
    def mnemonic_keyval(self, mnemonic_keyval=None):
        """
        Set the ``mnemonic_keyval`` property value

        :param mnemonic_keyval: The mnemonic accelerator key.
        :type mnemonic_keyval: int
        :raise TypeError: When ``mnemonic_keyval`` is not a int type or None
        """
        if mnemonic_keyval is None:
            mnemonic_keyval = 16777215
        if type(mnemonic_keyval) != int:
            raise TypeError(
                "'mnemonic_keyval' property value must be a int type or None"
            )
        if self.mnemonic_keyval != mnemonic_keyval:
            self.__mnemonic_keyval = mnemonic_keyval

    @property
    def mnemonic_widget(self):
        """
        The GLXCurses.Widget to be activated when the label's mnemonic key is pressed.

        :return: The GLXCurses.Widget to be activated or None if not set
        :rtype GLXCurses.Widget or None
        """
        return self.__mnemonic_widget

    @mnemonic_widget.setter
    def mnemonic_widget(self, mnemonic_widget=None):
        """
        Set the ``mnemonic_widget`` property value

        :param mnemonic_widget: The GLXCurses.Widget to be activated or None
        :type mnemonic_widget: GLXCurses.Widget or None
        :raise TypeError: When ``mnemonic_widget`` property value is not a GLXCurses.Widget or None
        """
        if mnemonic_widget is not None and not isinstance(
                mnemonic_widget, GLXCurses.Widget
        ):
            raise TypeError(
                "'mnemonic_widget' property value must be a GLXCurses.Widget or None"
            )
        if self.mnemonic_widget != mnemonic_widget:
            self.__mnemonic_widget = mnemonic_widget

    @property
    def pattern(self):
        """
        A string with _ characters in positions correspond to characters in the text to underline.

        :return: characters in the text use for underline
        :rtype: str
        """
        return self.__pattern

    @pattern.setter
    def pattern(self, pattern=None):
        """
        Set the ``pattern`` property value

        :param pattern: characters in the text use for underline
        :type pattern: str or None
        """
        if pattern is not None and type(pattern) != str:
            raise TypeError("'pattern' property value must be a str type or None")
        if self.pattern != pattern:
            self.__pattern = pattern

    @property
    def selectable(self):
        """
        Whether the GLXCurses.Label text can be selected with the mouse.

        :return: True if GLXCurses.Label text can be selected
        :rtype: bool
        """
        return self.__selectable

    @selectable.setter
    def selectable(self, selectable=None):
        """
        Set the ``selectable`` property value

        :param selectable: True if GLXCurses.Label text can be selected
        :type selectable: bool or None
        :raise TypeError: When ``selectable`` property value is not bool type or None
        """
        if selectable is None:
            selectable = False
        if type(selectable) != bool:
            raise TypeError("'selectable' property value must be bool type or None")
        if self.selectable != selectable:
            self.__selectable = selectable

    @property
    def selection_bound(self):
        """
        The position of the opposite end of the selection from the cursor in chars.

        :return: The position in chars
        :rtype: int
        """
        return self.__selection_bound

    @selection_bound.setter
    def selection_bound(self, selection_bound=None):
        """
        Set the ``selection_bound`` property value

        Allowed values: >= 0

        :param selection_bound: The position in chars
        :type selection_bound: int or None
        :raise TypeError: When ``selection_bound`` property value is not int type or None
        :raise ValueError: When ``selection_bound`` property value is not >= to 0
        """
        if selection_bound is None:
            selection_bound = 0
        if type(selection_bound) != int:
            raise TypeError("'selection_bound' must be a int type or None")
        if not selection_bound >= 0:
            raise ValueError("'selection_bound' must be >= to 0")
        if self.selection_bound != selection_bound:
            self.__selection_bound = selection_bound

    @property
    def single_line_mode(self):
        """
        Whether the label is in single line mode. In single line mode, the height of the label does not depend on the
        actual text, it is always set to ascent + descent of the font.

        This can be an advantage in situations where resizing the label because of text changes would be distracting,
        e.g. in a GLXCurses.StatusBar or GLXCurses.MessageBar.

        Default value: False

        :return: True if label is in single line mode
        :rtype: bool
        """
        return self.__single_line_mode

    @single_line_mode.setter
    def single_line_mode(self, single_line_mode=None):
        """
        Set the ``single_line_mode`` property value

        :param single_line_mode:True if label is in single line mode
        :type single_line_mode: bool or None
        :raise TypeError: When ``single_line_mode`` property value is not a bool type or None
        """
        if single_line_mode is None:
            single_line_mode = False
        if type(single_line_mode) != bool:
            raise TypeError(
                "'single_line_mode' property value must be a bool type or None"
            )
        if self.single_line_mode != single_line_mode:
            self.__single_line_mode = single_line_mode

    @property
    def track_visited_links(self):
        """
        Set this property to True to make the label track which links have been visited.

        It will then apply the GLXC.STATE_FLAG_VISITED when rendering this link, in addition to GLXC.STATE_FLAG_LINK.

        Default value: True

        :return: True if label track which links have been visited
        :rtype: bool
        """
        return self.__track_visited_links

    @track_visited_links.setter
    def track_visited_links(self, track_visited_links=None):
        """
        Set the ``track_visited_links`` property value

        :param track_visited_links: True if label track which links have been visited
        :type track_visited_links: bool or None
        :raise TypeError: When ``track_visited_links`` property value is not a bool type or None
        """
        if track_visited_links is None:
            track_visited_links = True
        if type(track_visited_links) != bool:
            raise TypeError(
                "'track_visited_links' property value must be a bool type or None"
            )
        if self.track_visited_links != track_visited_links:
            self.__track_visited_links = track_visited_links

    @property
    def use_markdown(self):
        """
        The text of the label includes TXT MarkDown.

        Default value: False

        :return: True if MarkDown is used
        :rtype: bool
        """
        return self.__use_markdown

    @use_markdown.setter
    def use_markdown(self, use_markdown=None):
        """
        Set the ``use_markdown`` property value

        :param use_markdown: True if MarkDown is used
        :type use_markdown: bool or None
        :raise TypeError: When ``use_markdown`` property value is not a bool type or None
        """
        if use_markdown is None:
            use_markdown = False
        if type(use_markdown) != bool:
            raise TypeError("'use_markdown' property value must be a bool type or None")
        if self.use_markdown != use_markdown:
            self.__use_markdown = use_markdown

    @property
    def use_underline(self):
        """
        If set, an underline in the text indicates the next character should be used for the mnemonic accelerator key.

        Default value: False

        :return: True if underline is display on text when use a mnemonic accelerator key
        :rtype: bool
        """
        return self.__use_underline

    @use_underline.setter
    def use_underline(self, use_underline=None):
        """
        Set the ``use_underline`` property value

        :param use_underline: if True a underline will be display on text when use a mnemonic accelerator key
        :type use_underline: bool or None
        :raise TypeError: When ``use_underline`` property value is not a bool type or None
        """
        if use_underline is None:
            use_underline = False
        if type(use_underline) != bool:
            raise TypeError(
                "'use_underline' property value must be a bool type or None"
            )
        if self.use_underline != use_underline:
            self.__use_underline = use_underline

    @property
    def width_chars(self):
        """
        The desired width of the label, in characters. If this property is set to -1, the width will be calculated
        automatically.

        See the section on text layout for details of how ``width_chars`` and ``max_width_chars`` determine the width
        of ellipsized and wrapped labels.

        :return: The desired width of the label, in characters.
        :rtype: int
        """
        return self.__width_chars

    @width_chars.setter
    def width_chars(self, width_chars=None):
        """
        Set the ``width_chars`` property value

        :param width_chars: The desired width of the label, in characters or None
        :type width_chars: int or None
        :raise TypeError: When ``width_chars`` property value is not a int type or None
        :raise ValueError: When ``width_chars`` property value is not >= to -1
        """
        if width_chars is None:
            width_chars = -1
        if type(width_chars) != int:
            raise TypeError("'width_chars' property value must be a int type or None")
        if not width_chars >= -1:
            raise ValueError("'width_chars' property value must be >= to -1")
        if self.width_chars != width_chars:
            self.__width_chars = width_chars

    @property
    def wrap(self):
        """
        If set, wrap lines if the text becomes too wide.

        :return: True if wrap is in use
        :rtype: bool
        """
        return self.__wrap

    @wrap.setter
    def wrap(self, wrap=None):
        """
        Set the ``wrap`` property value

        :param wrap: True if wrap is in use
        :type wrap: bool or None
        :raise TypeError: When ``wrap`` property value is not bool type or None
        """
        if wrap is None:
            wrap = False
        if type(wrap) != bool:
            raise TypeError("'wrap' property value must be bool type or None")
        if self.wrap != wrap:
            self.__wrap = wrap

    @property
    def wrap_mode(self):
        """
        If line wrapping is on (see the ``wrap`` property) this controls how the line wrapping is done.

        The default is GLXC.WRAP_WORD, which means wrap on word boundaries.

        :return: How the line wrapping is done
        :rtype: GLXCurses.GLXC.WrapMode
        """
        return self.__wrap_mode

    @wrap_mode.setter
    def wrap_mode(self, wrap_mode=None):
        """
        Set the ``wrap_mode`` property value

        :param wrap_mode: How the line wrapping is done or None
        :type wrap_mode: GLXCurses.GLXC.WrapMode
        """
        if wrap_mode is None:
            wrap_mode = GLXCurses.GLXC.WRAP_WORD
        if type(wrap_mode) != str:
            raise TypeError("'wrap_mode' property value must be a str type or None")
        if str(wrap_mode).upper() not in GLXCurses.GLXC.WrapMode:
            raise ValueError("'wrap_mode' must be a valid GLXC.WrapMode")
        if self.wrap_mode != wrap_mode:
            self.__wrap_mode = wrap_mode

    ###########
    # Methods #
    ###########
    def new(self, string=None):
        """
        Creates a new label with the given text inside it.

        You can pass None to get an empty GLXCurses.Label.

        :param string: The text of the GLXCurses.Label.
        :type string: str or None
        :return: The new GLXCurses.Label it self
        :rtype: GLXCurses.Label
        """
        self.__init__()
        if string:
            self.label = string
            self.use_markdown = False
            self.mnemonic_keyval = None
            self.mnemonic_widget = None
            self.justify = GLXCurses.GLXC.JUSTIFY_LEFT
            self.attributes = GLXCurses.TextAttributes().parse(
                label=self.label,
                markdown_is_used=self.use_markdown,
                mnemonic_is_used=False,
                mnemonic_char=self.pattern,
                mnemonic_use_underline=self.use_underline,
            )
        return self

    def set_text(self, string=None):
        """
        Sets the text within the GtkLabel widget. It overwrites any text that was there before.

        This function will clear any previously set mnemonic accelerators,
        and set the ``use_underline`` property to False as a side effect.

        This function will set the ``use_markdown`` property to False as a side effect.

        See also: GLXCurses.Label().set_markdown()

        :param string: The text you want to set
        :type string: str or None
        """
        self.label = string
        self.mnemonic_keyval = None
        self.mnemonic_widget = None
        self.use_underline = False
        self.use_markdown = False

    def set_attributes(self, attributes=None):
        """
        Sets a GLXC.StateFlags; the attributes in the list are applied to the label text.

        The attributes set with this function will be applied and merged with any other attributes previously effected
        by way of the ``use_underline`` or ``use_markup`` properties.

        While it is not recommended to mix markdown strings with manually set attributes, if you must; know that the
        attributes will be applied to the label after the markdown string is parsed.

        :param attributes: a GLXC.StateFlags
        :type attributes: list or None
        """
        self.attributes = attributes

    def set_markdown(self, string=None):
        """
        Parses ``string`` which is marked down with the text markdown language, setting the label’s text and
        attribute list based on the parse results.

        This function will set the ``use_markup`` property to ``True`` as a side effect.

        If you set the label contents using the ``label`` property you should also ensure that you set the
        ``use_markup`` property accordingly.

        See also: GLXCurses.Label().set_text()

        :param string: A markdown string (see text markdown format)
        :type string: str
        """
        self.label = string
        self.attributes = GLXCurses.TextAttributes().parse(
            label=self.label,
            markdown_is_used=True,
            mnemonic_char=self.pattern,
            mnemonic_use_underline=self.use_underline,
            mnemonic_is_used=False,
        )
        self.use_markdown = True
        if self.parent:
            self.mnemonic_widget = self.parent
        else:
            self.mnemonic_widget = self

    def set_markdown_with_mnemonic(self, string):
        """
        Parses ``string`` which is marked down with the text markdown language, setting the label’s text and
        attribute list based on the parse results.

        If characters in ``string`` are preceded by an underscore, they are
        underlined indicating that they represent a keyboard accelerator called a mnemonic.

        The mnemonic key can be used to activate another GLXCurses.Widget, chosen automatically, or explicitly using
        GLXCurses.Label().set_mnemonic_widget().

        :param string: A markdown string (see text markdown format)
        :type string: str
        """
        self.label = string
        self.use_markdown = True

        self.attributes = GLXCurses.TextAttributes().parse(
            label=self.label,
            markdown_is_used=self.use_markdown,
            mnemonic_is_used=True,
            mnemonic_char=self.pattern,
            mnemonic_use_underline=self.use_underline,
        )

        for item in self.attributes:
            if "MNEMONIC" in item and item["MNEMONIC"]:
                if "CHAR" in item and item["CHAR"]:
                    self.mnemonic_keyval = ord(item["CHAR"])

        if self.parent:
            self.mnemonic_widget = self.parent
        else:
            self.mnemonic_widget = self

    def set_pattern(self, pattern=None):
        """
        The pattern of underlines you want under the existing text within the GLXCurses.Label widget.

        For example if the current text of the label says “FooBarBaz” passing a pattern
        of “___ ___” will underline “Foo” and “Baz” but not “Bar”.

        :param pattern: The pattern as described above.
        :type pattern: str or None
        """
        self.pattern = pattern

    def set_justify(self, jtype=None):
        """
        Sets the alignment of the lines in the text of the label relative to each other.

        GLXCurses.GLXC.JUSTIFY_LEFT is the default value when the widget is first created with GLXCurses.Label().new()

        If you instead want to set the alignment of the label as a whole, use
        GLXCurses.Widget().set_halign() instead.

        GLXCurses.Label().set_justify() has no effect on labels containing only a single line.

        :param jtype: a GLXCurses.GLXC.Justification
        :type jtype: str or None
        """
        if not self.single_line_mode or len(str(self.label).split("\n")) > 1:
            self.justify = jtype
            if self.justify == GLXCurses.GLXC.JUSTIFY_CENTER:
                self.xalign = 0.5

            elif self.justify == GLXCurses.GLXC.JUSTIFY_RIGHT:
                self.xalign = 1.0

            elif self.justify == GLXCurses.GLXC.JUSTIFY_LEFT:
                self.xalign = 0.0

    def set_xalign(self, xalign=None):
        """
        Sets the ``xalign`` property for label .

        :param xalign: the new xalign value, between 0 and 1
        :type xalign: float or None
        """
        self.xalign = xalign

    def set_yalign(self, yalign=None):
        """
        Sets the ``yalign`` property for label .

        :param yalign: the new yalign value, between 0 and 1
        :type yalign: float or None
        """
        self.yalign = yalign

    def set_width_chars(self, n_chars=None):
        """
        Sets the desired width in characters of label to ``n_chars`` .

        :param n_chars: the new desired width, in characters.
        :type n_chars: int or None
        """
        self.width_chars = n_chars

    def set_max_width_chars(self, n_chars):
        """
        Sets the desired maximum width in characters of label to ``n_chars`` .

        :param n_chars: the new desired maximum width, in characters.
        :type n_chars: int or None
        """
        self.max_width_chars = n_chars

    def set_line_wrap(self, wrap=None):
        """
        Toggles line wrapping within the GtkLabel widget.
        ``True`` makes it break lines if text exceeds the widget’s size.
        ``False`` lets the text get cut off by the edge of the widget if it exceeds the widget size.

        Note that setting line wrapping to TRUE does not make the label wrap at its parent container’s width,
        because GLXCurses widgets conceptually can’t make their requisition depend on the parent container’s size.
        For a label that wraps at a specific position, set the label’s width using
        GLXCurses.Widget().set_size_request()

        :param wrap: True if wrap is enable
        :type wrap: bool or None
        """
        self.wrap = wrap

    def set_line_wrap_mode(self, wrap_mode=None):
        """
        If line wrapping is on (see GLXCurses.Label().set_line_wrap()) this controls how the line wrapping is done.
        The default is GLXCurses.GLXC.WRAP_WORD which means wrap on word boundaries.

        :param wrap_mode: the line wrapping mode
        :type wrap_mode: str or None
        """
        self.wrap_mode = wrap_mode

    def set_lines(self, lines=None):
        """
        Sets the number of lines to which an ellipsized, wrapping label should be limited.
        This has no effect if the label is not wrapping or ellipsized.

        Set this to -1 if you don’t want to limit the number of lines.

        :param lines: the desired number of lines, or -1
        :type lines: int or None
        """
        self.lines = lines

    def get_mnemonic_keyval(self):
        """
        If the label has been set so that it has an mnemonic key this function returns the keyval used for
        the mnemonic accelerator.

        If there is no mnemonic set up it returns ``None``.

        :return: ord() keyval usable for accelerators, or None
        :rtype: int or None
        """
        return self.mnemonic_keyval

    def get_selectable(self):
        """
        Gets the value set by GLXCurses.Label().set_selectable().

        :return: ``True`` if the user can copy text from the label
        """
        return self.selectable

    def get_text(self):
        """
        Fetches the text from a label widget, as displayed on the screen.

        This does not include any embedded underlines indicating mnemonics or markdown.

        (See GLXCurses.Label().get_label())

        :return: the text in the label widget. This is the internal string used by the label, and must not be modified.
        :rtype: str or None
        """
        tmp_label = ""
        count = 0
        while count <= len(self.attributes) - 1:
            if not self.attributes[count]["HIDDEN"]:
                tmp_label += self.attributes[count]["CHAR"]
            count += 1
        return tmp_label

    def new_with_mnemonic(self, string=None):
        """
        Creates a new GtkLabel, containing the text in str .

        If characters in str are preceded by an underscore, they are underlined.
        If you need a literal underscore character in a label, use '__' (two underscores).
        The first underlined character represents a keyboard accelerator called a mnemonic.
        The mnemonic key can be used to activate another widget, chosen automatically,
        or explicitly using gtk_label_set_mnemonic_widget().

        If GLXCurses.Label().set_mnemonic_widget() is not called,
        then the first activatable ancestor of the GLXCurses.Label will be chosen as the mnemonic widget.
        For instance, if the label is inside a button or menu item,
        the button or menu item will automatically become the mnemonic widget and be activated by the mnemonic.

        :param string: The text of the label, with an underscore in front of the mnemonic character.
        :type string: str or None
        """
        self.label = string
        self.use_markdown = False
        self.attributes = GLXCurses.TextAttributes().parse(
            label=self.label,
            markdown_is_used=self.use_markdown,
            mnemonic_is_used=True,
            mnemonic_use_underline=self.use_underline,
            mnemonic_char=self.pattern,
        )

        if self.parent:
            self.mnemonic_widget = self.parent

    def select_region(self, start_offset=None, end_offset=None):
        """
        Selects a range of characters in the label, if the label is selectable. See GLXCurses.Label().set_selectable().

        If the label is not selectable, this function has no effect.
        If ``start_offset`` or ``end_offset`` are -1, then the end of the label will be substituted.

        :param start_offset: start offset (in characters not bytes)
        :type start_offset: int
        :param end_offset: end offset (in characters not bytes)
        :type end_offset: int
        :raise TypeError: when
        """
        if type(start_offset) != int:
            raise TypeError("'start_offset' value must be a int type")
        if type(end_offset) != int:
            raise TypeError("'end_offset' value must be a int type")
        if self.selectable:
            if start_offset == -1:
                self.cursor_position = 0
            else:
                self.cursor_position = start_offset
            if end_offset == -1:
                self.selection_bound = len(self.get_text()) - 1
            else:
                self.selection_bound = end_offset

    # The set_use_underline() method sets the "use-underline" property to the value of setting.
    # If setting is True,
    # an underscore in the text indicates the next character should be used for the mnemonic accelerator key.
    def set_use_underline(self, setting):
        self.use_underline = setting

    # The get_use_underline() method returns the value of the "use-underline" property.
    # If True an embedded underscore in the label indicates the next character is a mnemonic. See set_use_underline().
    def get_use_underline(self):
        return self.use_underline

    # set_markup_with_mnemonic

    # The set_mnemonic_widget() method sets the "mnemonic-widget" property using the value of widget.
    # This method associates the label mnemonic with a widget that will be activated
    #   when the mnemonic accelerator is pressed.
    # When the label is inside a widget (like a Button or a Notebook tab) it is automatically associated
    #  with the correct widget, but sometimes (i.e. when the target is a gtk.Entry next to the label)
    #  you need to set it explicitly using this function.
    # The target widget will be activated by emitting "mnemonic_activate" on it.
    def set_mnemonic_widget(self, widget):
        self.mnemonic_widget = widget

    # The get_mnemonic_widget() method retrieves the value of the "mnemonic-widget" property which is the target
    # of the mnemonic accelerator of this label.
    # See set_mnemonic_widget().
    def get_mnemonic_widget(self):
        return self.mnemonic_widget

    def set_selectable(self, setting=None):
        """
        Selectable labels allow the user to select text from the label, for copy-and-paste.

        :param setting: ``True`` to allow selecting text in the label
        :type setting: bool or None
        """
        self.selectable = setting

    def set_text_with_mnemonic(self, string):
        """
        Sets the label’s text from the string str .
        If characters in str are preceded by an underscore, they are underlined indicating that they represent a
        keyboard accelerator called a mnemonic.

        The mnemonic key can be used to activate another widget, chosen automatically, or explicitly using
        GLXCurses.Label().set_mnemonic_widget().

        :param string: a string
        :type string: str
        """
        self.label = string
        self.use_markdown = False
        self.attributes = GLXCurses.TextAttributes().parse(
            label=self.label,
            markdown_is_used=self.use_markdown,
            mnemonic_is_used=True,
            mnemonic_char=self.pattern,
            mnemonic_use_underline=self.use_underline,
        )

        for item in self.attributes:
            if "MNEMONIC" in item and item["MNEMONIC"]:
                if "CHAR" in item and item["CHAR"]:
                    self.mnemonic_keyval = ord(item["CHAR"])

        if self.parent:
            self.mnemonic_widget = self.parent
        else:
            self.mnemonic_widget = self

    def draw_widget_in_area(self):
        self.update_preferred_sizes()

        if self.label:
            if self.single_line_mode:
                self._draw_single_line_mode()
            else:
                self._draw_multi_line_mode()

    def update_preferred_sizes(self):
        preferred_width = 0
        preferred_height = 0

        if self.label:
            preferred_width += len(self.label)
            if self._get_imposed_spacing():
                preferred_width += self._get_imposed_spacing() * 2

        if self.single_line_mode:
            preferred_height += 1
            if self._get_imposed_spacing():
                preferred_height += self._get_imposed_spacing() * 2
        elif self.wrap_mode:
            preferred_height += 1
            if self._get_imposed_spacing():
                preferred_height += self._get_imposed_spacing() * 2

        self.preferred_height = preferred_height
        self.preferred_width = preferred_width

    def get_justify(self):
        """
        Returns the justification of the label.

        .. seealso:: \
        :func:`Label.set_justify() <GLXCurses.Label.Label.set_justify()>` for set the justification.

        :return: the justification
        :rtype: GLXCurses.GLXC.Justification
        """
        return self.justify

    def get_line_wrap(self):
        """
        The get_line_wrap() method returns the value of the "wrap" property.

        If "wrap" is True the lines in the label are automatically wrapped. See set_line_wrap().

        :return: True if wrap is enable
        :rtype: bool
        """
        return self.wrap

    def get_width_chars(self):
        """
        The get_width_chars() method returns the value of the ``width-chars``

        property that specifies the desired width of the label in characters.

        :return: width of the label in characters
        :rtype: int
        """
        return self.width_chars

    # The set_single_line_mode() method sets the "single-line-mode" property to the value of single_line_mode.
    # If single_line_mode is True the label is in single line mode where the height of the label does not
    # depend on the actual text, it is always set to ascent + descent of the font.
    def set_single_line_mode(self, single_line_mode):
        self.single_line_mode = bool(single_line_mode)

    # The get_single_line_mode() method returns the value of the "single-line-mode" property.
    # See the set_single_line_mode() method for more information
    def get_single_line_mode(self):
        return bool(self.single_line_mode)

    # The get_max_width_chars() method returns the value of the "max-width-chars" property
    # which is the desired maximum width of the label in characters.
    def get_max_width_chars(self):
        return self.max_width_chars

    def get_line_wrap_mode(self):
        return self.wrap_mode

    # Internal
    def _draw_single_line_mode(self):
        # Single line ignore markdown as describe on GTK3 doc
        # text = GLXCurses.resize_text(text=self.get_text(), max_width=self.width)

        position = 0
        item_number = 0

        while item_number <= len(self.attributes) - 1:
            if not self.attributes[item_number]["HIDDEN"]:
                # Draw
                self.add_character(
                    y=GLXCurses.clamp(
                        value=int(self.height * self.yalign),
                        smallest=0,
                        largest=self.height - 1,
                    ),
                    x=GLXCurses.clamp(
                        value=int((self.width - len(self.get_text())) * self.xalign)
                              + position,
                        smallest=0,
                        largest=self.width,
                    ),
                    character=self.attributes[item_number]["CHAR"],
                    color=self.color_normal
                          | self.attributes[item_number]["CURSES_ATTRIBUTES"],
                )
                position += 1
            # Finally
            item_number += 1

    def _draw_multi_line_mode(self):

        max_height = self.height - 1 - (self.ypad * 2)
        max_width = self.width - (self.xpad * 2)

        line_number = 0
        for line in self._textwrap(text=self.label, height=max_height, width=max_width):
            char_number = 0
            for char in line:
                self.add_character(
                    y=GLXCurses.clamp(value=int(self.height * self.yalign) + line_number,
                                      smallest=0,
                                      largest=max_height,
                                      ),
                    x=GLXCurses.clamp(value=int((self.width - len(line)) * self.xalign) + char_number,
                                      smallest=0,
                                      largest=max_width,
                                      ),
                    character=char,
                    color=self.color_normal,
                )
                char_number += 1
            line_number += 1

    def _textwrap(self, text="Hello World!", height=24, width=80):
        if self.get_line_wrap():
            lines = []
            for paragraph in text.split("\n"):
                line = []
                len_line = 0
                if self.get_line_wrap_mode() == GLXCurses.GLXC.WRAP_WORD_CHAR:
                    # Wrap this text.
                    wrapped = textwrap.wrap(
                        paragraph,
                        width=width,
                        fix_sentence_endings=True,
                        break_long_words=True,
                        break_on_hyphens=True,
                    )

                    if len(lines) <= height:
                        lines += wrapped
                elif self.get_line_wrap_mode() == GLXCurses.GLXC.WRAP_CHAR:
                    if len(paragraph) < width:
                        if len(lines) < height:
                            lines.append(paragraph)
                    else:
                        if len(lines) < height:
                            lines += [
                                paragraph[ind: ind + width]
                                for ind in range(0, len(paragraph), width)
                            ]
                else:
                    for word in paragraph.split(" "):
                        len_word = len(word)
                        if len_line + len_word <= width:
                            line.append(word)
                            len_line += len_word + 1
                        else:
                            lines.append(" ".join(line))
                            line = [word]
                            len_line = len_word + 1

                    if len(lines) < height:
                        lines.append(" ".join(line))
            return lines
        else:
            # This is the default display/view
            lines = []
            for paragraph in text.split("\n"):
                if len(paragraph) < width:
                    if len(lines) < height:
                        lines.append(paragraph)
                else:
                    if len(lines) < height:
                        lines.append(paragraph[:width])
            return lines

    def _check_justification(self, text="Hello World!", width=80):
        # Check Justification
        self.text_x = 0
        if self.justify == GLXCurses.GLXC.JUSTIFY_CENTER:
            self.xalign = 0.0
            return text.center(width, " ")
        elif self.justify == GLXCurses.GLXC.JUSTIFY_LEFT:
            self.xalign = 0.0
            return "{0:<{1}}".format(text, width)
        elif self.justify == GLXCurses.GLXC.JUSTIFY_RIGHT:
            self.xalign = 0.0
            return "{0:>{1}}".format(text, width)
        else:
            self.xalign = int((self.width - len(self.get_text())) * self.xalign)
            self.yalign = int(self.height * self.yalign)
        return self.text_x
