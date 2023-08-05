#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

from GLXCurses import GLXC
import textwrap
import re

NEWLINE = re.compile(r"\n+")


class TextUtils(object):
    def __init__(self):

        self.__height = None
        self.__lines = None
        self.__text = None
        self.__width = None
        self.__wrap = None
        self.__wrap_mode = None

        self.height = None
        self.lines = None
        self.text = None
        self.width = None
        self.wrap = None
        self.wrap_mode = None

    @property
    def height(self):
        """
        Get :py:obj:`height` property value.

        :return: :py:obj:`height` property
        :rtype: int or None
        """
        return self.__height

    @height.setter
    def height(self, height=None):
        """
        Set ``height`` property value.

        :param height: :py:obj:`height` property value
        :type height: int or None
        :raise TypeError: if ``height`` parameter is not a :py:data:`int` type or None
        """
        if height is None:
            height = 24
        if height is not None and type(height) != int:
            raise TypeError("'height' argument must be a int type or None")
        if self.height != height:
            self.__height = height

    @property
    def lines(self):
        """
        The lines
        This property has no effect if the text is not wrapping .

        :return: Lines dispatch on by list item
        :rtype: list
        """
        return self.__lines

    @lines.setter
    def lines(self, lines=None):
        """
        Set the ``lines`` property value

        :param lines: Lines dispatch on by list item
        :type lines: list
        :raise TypeError: When ``lines`` property is not a list type or None
        """
        if lines is None:
            lines = []
        if type(lines) != list:
            raise TypeError("'lines' property value must be list type or None")
        if self.lines != lines:
            self.__lines = lines

    @property
    def text(self):
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
        return self.__text

    @text.setter
    def text(self, text=None):
        """
        Set the ``text`` property value

        :param text: Contents of the label
        :type text: str or None
        :raise TypeError: When ``text`` property value is not str type or None
        """
        if text is None:
            text = ""
        if type(text) != str:
            raise TypeError('"text" must be a str type or None')
        if self.text != text:
            self.__text = text

    @property
    def width(self):
        """
        Get :py:obj:`width` property value.

        :return: :py:obj:`width` property
        :rtype: int or None
        """
        return self.__width

    @width.setter
    def width(self, width=None):
        """
        Set :py:obj:`width` property value.

        :param width: :py:obj:`width` property value
        :type width: int or None
        :raise TypeError: if ``width`` parameter is not a :py:data:`int` type or None
        """
        if width is None:
            width = 80
        if width is not None and not isinstance(width, int):
            raise TypeError("'width' argument must be a int type or None")
        if self.width != width:
            self.__width = width

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
        :rtype: GLXC.WrapMode
        """
        return self.__wrap_mode

    @wrap_mode.setter
    def wrap_mode(self, wrap_mode=None):
        """
        Set the ``wrap_mode`` property value

        :param wrap_mode: How the line wrapping is done or None
        :type wrap_mode: GLXC.WrapMode
        """
        if wrap_mode is None:
            wrap_mode = GLXC.WRAP_WORD
        if type(wrap_mode) != str:
            raise TypeError("'wrap_mode' property value must be a str type or None")
        if str(wrap_mode).upper() not in GLXC.WrapMode:
            raise ValueError("'wrap_mode' must be a valid GLXC.WrapMode")
        if self.wrap_mode != wrap_mode:
            self.__wrap_mode = wrap_mode

    def scan(self):
        pass

    def text_wrap(self, height=None, width=None):
        if height is None:
            height = self.height
        if width is None:
            width = self.width

        self.lines = None

        if self.wrap:

            for line in re.split(NEWLINE, self.text)[:-1]:
                len_line = 0
                if self.wrap_mode == GLXC.WRAP_WORD_CHAR:
                    # Wrap this text.
                    wrapped = textwrap.wrap(
                        line,
                        width=width,
                        fix_sentence_endings=True,
                        break_long_words=True,
                        break_on_hyphens=True,
                    )

                    if len(self.lines) <= height:
                        self.lines += wrapped
                elif self.wrap_mode == GLXC.WRAP_CHAR:
                    if len(line) < self.width:
                        if len(self.lines) < height:
                            self.lines.append(line)
                    else:
                        if len(self.lines) < height:
                            self.lines += [
                                line[ind : ind + width]
                                for ind in range(0, len(line), width)
                            ]
                else:
                    final_line = []
                    for word in line.split(" "):
                        len_word = len(word)
                        if len_line + len_word <= width:
                            final_line.append(word)
                            len_line += len_word + 1
                        # else:
                            # final_line.append("".join(line))
                            # line = [word]
                            # len_line = len_word + 1

                    if len(self.lines) < height:
                        self.lines.append(" ".join(final_line))

        else:
            # This is the default display/view
            for line in re.split(NEWLINE, self.text)[:-1]:
                self.lines.append(line)

        return self.lines
