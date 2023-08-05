#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
from GLXCurses import GLXC as GLXC


class TextAttributes(object):
    def __init__(self):
        self.__attributes = None
        self.__label = None
        self.__markdown_is_used = None
        self.__mnemonic_char = None
        self.__mnemonic_is_used = None
        self.__mnemonic_use_underline = None

        # First init
        self.attributes = None
        self.label = None
        self.markdown_is_used = None
        self.mnemonic_char = None
        self.__mnemonic_is_used = None
        self.mnemonic_use_underline = None

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
    def markdown_is_used(self):
        """
        Get the ``markdown_is_used`` property value

        Default value: False

        :return: if True the contain of ``label`` property is consider as MarkDown
        :rtype: bool
        """
        return self.__markdown_is_used

    @markdown_is_used.setter
    def markdown_is_used(self, markdown_is_used=None):
        """
        Set the ``markdown_is_used`` property value

        :param markdown_is_used: if True the contain of ``label`` property is consider as MarkDown
        :type markdown_is_used: bool or None
        :raise TypeError: When ``markdown_is_used`` property value is not a bool type or None
        """
        if markdown_is_used is None:
            markdown_is_used = False
        if type(markdown_is_used) != bool:
            raise TypeError(
                "'markdown_is_used' property value must be a bool type or None"
            )
        if self.markdown_is_used != markdown_is_used:
            self.__markdown_is_used = markdown_is_used

    @property
    def mnemonic_char(self):
        """
        A string with _ characters in positions correspond to characters in the text to underline.

        :return: characters in the text use for underline
        :rtype: str
        """
        return self.__mnemonic_char

    @mnemonic_char.setter
    def mnemonic_char(self, mnemonic_char=None):
        """
        Set the ``pattern`` property value

        Default value: ``_``

        :param mnemonic_char: character in the text use for underline
        :type mnemonic_char: str or None
        """
        if mnemonic_char is None:
            mnemonic_char = "_"
        if mnemonic_char is not None and type(mnemonic_char) != str:
            raise TypeError("'mnemonic_char' property value must be a str type or None")
        if mnemonic_char is not None and len(mnemonic_char) > 1:
            raise ValueError(
                "'mnemonic_char' property value must be a str type or None"
            )
        if self.mnemonic_char != mnemonic_char:
            self.__mnemonic_char = mnemonic_char

    @property
    def mnemonic_is_used(self):
        """
        Get the ``mnemonic_is_used`` property value

        Default value: False

        :return: if True the contain of ``label`` property is consider as MarkDown
        :rtype: bool
        """
        return self.__mnemonic_is_used

    @mnemonic_is_used.setter
    def mnemonic_is_used(self, mnemonic_is_used=None):
        """
        Set the ``mnemonic_is_used`` property value

        :param mnemonic_is_used: if True the contain of ``label`` property is consider as MarkDown
        :type mnemonic_is_used: bool or None
        :raise TypeError: When ``mnemonic_is_used`` property value is not a bool type or None
        """
        if mnemonic_is_used is None:
            mnemonic_is_used = False
        if type(mnemonic_is_used) != bool:
            raise TypeError(
                "'mnemonic_is_used' property value must be a bool type or None"
            )
        if self.mnemonic_is_used != mnemonic_is_used:
            self.__mnemonic_is_used = mnemonic_is_used

    @property
    def mnemonic_use_underline(self):
        """
        If set, an underline in the text indicates the next character should be used for the mnemonic accelerator key.

        Default value: False

        :return: True if underline is display on text when use a mnemonic accelerator key
        :rtype: bool
        """
        return self.__mnemonic_use_underline

    @mnemonic_use_underline.setter
    def mnemonic_use_underline(self, mnemonic_use_underline=None):
        """
        Set the ``use_underline`` property value

        :param mnemonic_use_underline: if True a underline will be display on text when use a mnemonic accelerator key
        :type mnemonic_use_underline: bool or None
        :raise TypeError: When ``use_underline`` property value is not a bool type or None
        """
        if mnemonic_use_underline is None:
            mnemonic_use_underline = False
        if type(mnemonic_use_underline) != bool:
            raise TypeError(
                "'mnemonic_use_underline' property value must be a bool type or None"
            )
        if self.mnemonic_use_underline != mnemonic_use_underline:
            self.__mnemonic_use_underline = mnemonic_use_underline

    def new(self):
        """
        Create a new GLXCurses.TextAttributes object and return it

        :return: a new GLXCurses.TextAttributes
        :rtype: GLXCurses.TextAttributes
        """
        self.__init__()
        return self

    def prepare_attributes(self):
        self.attributes = []
        for position in range(0, len(self.label)):
            self.attributes.append(
                {
                    "A_ALTCHARSET": False,
                    "A_BLINK": False,
                    "A_BOLD": False,
                    "A_CHARTEXT": False,
                    "A_DIM": False,
                    "A_INVIS": False,
                    "A_NORMAL": False,
                    "A_REVERSE": False,
                    "A_STANDOUT": False,
                    "A_UNDERLINE": False,
                    "A_PROTECT": False,
                    "A_ITALIC": False,
                    "CHAR": str(self.label)[position],
                    "CURSES_ATTRIBUTES": 0,
                    "HIDDEN": False,
                    "MNEMONIC": False,
                }
            )

    def parse_markdown_with_mnemonic(self):
        self.prepare_attributes()

        bold_is_open = False
        italic_is_open = False
        underline_is_open = False
        mnemonic_is_open = False
        mnemonic_locked = False
        position = 0

        while position <= len(self.attributes) - 2:
            # BOLD
            if (
                "*" in self.attributes[position]["CHAR"]
                and "*" in self.attributes[position + 1]["CHAR"]
            ):
                bold_is_open = not bold_is_open
                self.attributes[position]["HIDDEN"] = True
                self.attributes[position + 1]["HIDDEN"] = True
                position += 2
                continue
            # UNDERLINE
            elif (
                "+" in self.attributes[position]["CHAR"]
                and "+" in self.attributes[position + 1]["CHAR"]
            ):
                underline_is_open = not underline_is_open
                self.attributes[position]["HIDDEN"] = True
                self.attributes[position + 1]["HIDDEN"] = True
                position += 2
                continue
            # ITALIC
            elif "*" in self.attributes[position]["CHAR"]:
                italic_is_open = not italic_is_open
                self.attributes[position]["HIDDEN"] = True
                position += 1
                continue
            # MNEMONIC
            elif self.mnemonic_char in self.attributes[position]["CHAR"]:
                mnemonic_is_open = True
                self.attributes[position]["HIDDEN"] = True
                position += 1
                continue

            # Set variables
            else:
                if mnemonic_is_open and not mnemonic_locked:
                    self.attributes[position]["MNEMONIC"] = True
                    if self.mnemonic_use_underline:
                        self.attributes[position]["UNDERLINE"] = True
                    mnemonic_locked = True
                if bold_is_open:
                    self.attributes[position]["A_BOLD"] = True
                if italic_is_open:
                    self.attributes[position]["A_ITALIC"] = True
                if underline_is_open:
                    self.attributes[position]["A_UNDERLINE"] = True

            # Finally
            position += 1

    def parse_markdown_with_no_mnemonic(self):
        self.prepare_attributes()
        bold_is_open = False
        italic_is_open = False
        underline_is_open = False
        position = 0

        while position <= len(self.attributes) - 2:

            # BOLD
            if (
                "*" in self.attributes[position]["CHAR"]
                and "*" in self.attributes[position + 1]["CHAR"]
                or "_" in self.attributes[position]["CHAR"]
                and "_" in self.attributes[position + 1]["CHAR"]
            ):
                bold_is_open = not bold_is_open
                self.attributes[position]["HIDDEN"] = True
                self.attributes[position + 1]["HIDDEN"] = True
                position += 2
                continue

            # ITALIC
            elif (
                "*" in self.attributes[position]["CHAR"]
                or "_" in self.attributes[position]["CHAR"]
            ):
                italic_is_open = not italic_is_open
                self.attributes[position]["HIDDEN"] = True
                position += 1
                continue

            # UNDERLINE
            elif (
                "+" in self.attributes[position]["CHAR"]
                and "+" in self.attributes[position + 1]["CHAR"]
            ):
                underline_is_open = not underline_is_open
                self.attributes[position]["HIDDEN"] = True
                self.attributes[position + 1]["HIDDEN"] = True
                position += 2
                continue

            # Set variables
            else:
                if bold_is_open:
                    self.attributes[position]["A_BOLD"] = True
                if italic_is_open:
                    self.attributes[position]["A_ITALIC"] = True
                if underline_is_open:
                    self.attributes[position]["A_UNDERLINE"] = True

            # Finally
            position += 1

    def parse_text(self):
        self.prepare_attributes()
        if self.mnemonic_is_used:
            mnemonic_is_open = False
            mnemonic_locked = False
            position = 0

            while position <= len(self.label) - 1:
                # MNEMONIC
                if (
                    self.mnemonic_char in str(self.label)[position]
                    and not mnemonic_is_open
                ):
                    mnemonic_is_open = True
                    self.attributes[position]["HIDDEN"] = True
                    position += 1
                    continue

                # Set variables
                else:
                    if mnemonic_is_open and not mnemonic_locked:
                        self.attributes[position]["MNEMONIC"] = True
                        if self.mnemonic_use_underline:
                            self.attributes[position]["A_UNDERLINE"] = True
                        mnemonic_locked = True

                # Finally
                position += 1
        else:
            pass

    def parse(
        self,
        label=None,
        markdown_is_used=None,
        mnemonic_is_used=None,
        mnemonic_char=None,
        mnemonic_use_underline=None,
    ):

        self.label = label
        self.markdown_is_used = markdown_is_used
        self.mnemonic_is_used = mnemonic_is_used
        self.mnemonic_char = mnemonic_char
        self.mnemonic_use_underline = mnemonic_use_underline

        if self.markdown_is_used:
            if self.mnemonic_is_used:
                self.parse_markdown_with_mnemonic()
            else:
                self.parse_markdown_with_no_mnemonic()
        else:
            self.parse_text()

        for item in self.attributes:
            if "CURSES_ATTRIBUTES" in item and item["CURSES_ATTRIBUTES"]:
                item["CURSES_ATTRIBUTES"] = 0
            if "A_ALTCHARSET" in item and item["A_ALTCHARSET"]:
                item["CURSES_ATTRIBUTES"] = (
                    item["CURSES_ATTRIBUTES"] | GLXC.A_ALTCHARSET
                )
            if "A_BLINK" in item and item["A_BLINK"]:
                item["CURSES_ATTRIBUTES"] = item["CURSES_ATTRIBUTES"] | GLXC.A_BLINK
            if "A_BOLD" in item and item["A_BOLD"]:
                item["CURSES_ATTRIBUTES"] = item["CURSES_ATTRIBUTES"] | GLXC.A_BOLD
            if "A_CHARTEXT" in item and item["A_CHARTEXT"]:
                item["CURSES_ATTRIBUTES"] = item["CURSES_ATTRIBUTES"] | GLXC.A_CHARTEXT
            if "A_DIM" in item and item["A_DIM"]:
                item["CURSES_ATTRIBUTES"] = item["CURSES_ATTRIBUTES"] | GLXC.A_DIM
            if "A_INVIS" in item and item["A_INVIS"]:
                item["CURSES_ATTRIBUTES"] = item["CURSES_ATTRIBUTES"] | GLXC.A_INVIS
            if "A_NORMAL" in item and item["A_NORMAL"]:
                item["CURSES_ATTRIBUTES"] = item["CURSES_ATTRIBUTES"] | GLXC.A_NORMAL
            if "A_PROTECT" in item and item["A_PROTECT"]:
                item["CURSES_ATTRIBUTES"] = item["CURSES_ATTRIBUTES"] | GLXC.A_PROTECT
            if "A_REVERSE" in item and item["A_REVERSE"]:
                item["CURSES_ATTRIBUTES"] = item["CURSES_ATTRIBUTES"] | GLXC.A_REVERSE
            if "A_STANDOUT" in item and item["A_STANDOUT"]:
                item["CURSES_ATTRIBUTES"] = item["CURSES_ATTRIBUTES"] | GLXC.A_STANDOUT
            if "A_UNDERLINE" in item and item["A_UNDERLINE"]:
                item["CURSES_ATTRIBUTES"] = item["CURSES_ATTRIBUTES"] | GLXC.A_UNDERLINE
            if "A_ITALIC" in item and item["A_ITALIC"]:
                item["CURSES_ATTRIBUTES"] = item["CURSES_ATTRIBUTES"] | GLXC.A_ITALIC

        return self.attributes
