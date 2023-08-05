#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import GLXCurses
import curses
import logging


# Reference Document: https://developer.gnome.org/gtk3/stable/GtkFrame.html
class Frame(GLXCurses.Bin):
    """
    :Description:

    The frame widget is a bin that surrounds its child with a decorative frame and an optional label.
    If present, the label is drawn in a gap in the top side of the frame.

    The position of the label can be
    controlled with :func:`Frame.set_label_align() <GLXCurses.Frame.Frame.set_label_align()>`.
    """

    def __init__(self):
        # Load heritage
        GLXCurses.Bin.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = "GLXCurses.Frame"
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        # Make a Widget Style heritage attribute as local attribute
        # if self.style.attribute_states:
        #     if self.attribute_states != self.style.attribute_states:
        #         self.attribute_states = self.style.attribute_states

        self.preferred_height = 2
        self.preferred_width = 2

        self.set_decorated(1)
        self.set_border_width(1)
        self._set_imposed_spacing(1)

        ####################
        # Frame Attribute  #
        ####################
        self.__label = None
        self.__label_widget = None
        self.__label_xalign = None
        self.__label_yalign = None
        self.__shadow_type = None

        self.label = None
        self.label_widget = None
        self.label_xalign = 0.0
        self.label_yalign = 0.0
        self.shadow_type = GLXCurses.GLXC.SHADOW_NONE

    # def draw(self):
    #     self.y, self.x = self.get_parent_origin()
    #     self.height, self.width = self.get_parent_size()
    #     self.set_preferred_width(2)
    #     self.set_preferred_height(2)
    #     self.draw_widget_in_area()

    # GLXC Frame Functions
    @property
    def label(self):
        """
        Text of the frame's label.

        Default value: None

        :return: the ``label`` property value
        :rtype: str or None
        """
        return self.__label

    @label.setter
    def label(self, label=None):
        """
        Removes the current ``label_widget``.

        If label is not ``None``, creates a new GLXCurses.Label with that text and adds it as the ``label-widget``.

        :param label: the text to use as the label of the frame.
        :type label: str or None
        :raise TypeError: when ``label`` is not a str type or None
        """
        if type(label) != str and label is not None:
            raise TypeError('"label" must be a str type or None')

        if self.label != label:
            self.__label = label

        if self.label:
            self.label_widget = GLXCurses.Label()
            self.label_widget.set_single_line_mode(True)
            self.label_widget.set_markdown(self.label)
            self.label_widget.xalign = self.label_xalign
            self.label_widget.yalign = self.label_yalign
        else:
            self.label_widget = None

    @property
    def label_widget(self):
        """
        A widget to display in place of the usual frame label.

        :return: A widget
        :rtype: GLXCurses.Label or None
        """
        return self.__label_widget

    @label_widget.setter
    def label_widget(self, label_widget=None):
        """
        Set the ``label_widget`` property value

        :param label_widget: A widget to display in place of the usual frame label.
        :type label_widget: GLXCurses.Label or None
        :raise TypeError: when ``label_widget`` is not a GLXCurses.Widget instance or None
        """
        if (
            label_widget is not None
            and not isinstance(label_widget, GLXCurses.Label)
            and not isinstance(label_widget, GLXCurses.Widget)
        ):
            raise TypeError(
                "'label_widget' must be None or a GLXCurses.Widget instance"
            )

        if self.label_widget != label_widget:
            self.__label_widget = label_widget

    @property
    def label_xalign(self):
        """
        The horizontal alignment of the label.

        :return: The horizontal alignment of the label.
        :rtype: float
        """
        return self.__label_xalign

    @label_xalign.setter
    def label_xalign(self, label_xalign=None):
        """
        Set the ``label_xalign`` property value

        :param label_xalign: horizontal alignment
        :type label_xalign: float or None
        :raise TypeError: when ``label_xalign`` is not a float type or None
        """
        if label_xalign is None:
            label_xalign = 0.0
        if type(label_xalign) != float:
            raise TypeError("'label_xalign' must be a float type or None")
        if self.label_xalign != GLXCurses.clamp(
            value=label_xalign, smallest=0.0, largest=1.0
        ):
            self.__label_xalign = GLXCurses.clamp(
                value=label_xalign, smallest=0.0, largest=1.0
            )
        if self.label_widget:
            self.label_widget.xalign = self.label_xalign

    @property
    def label_yalign(self):
        """
        The vertical alignment of the label.

        :return: The vertical alignment of the label.
        :rtype: float
        """
        return self.__label_yalign

    @label_yalign.setter
    def label_yalign(self, label_yalign=None):
        """
        Set the ``label_xalign`` property value

        :param label_yalign: vertical alignment
        :type label_yalign: float or None
        :raise TypeError: when ``label_yalign`` is not a float type or None
        """
        if label_yalign is None:
            label_yalign = 0.5
        if type(label_yalign) != float:
            raise TypeError("'label_yalign' must be a float type or None")
        if self.label_yalign != GLXCurses.clamp(
            value=label_yalign, smallest=0.0, largest=1.0
        ):
            self.__label_yalign = GLXCurses.clamp(
                value=label_yalign, smallest=0.0, largest=1.0
            )
        if self.label_widget:
            self.label_widget.yalign = self.label_yalign

    @property
    def shadow_type(self):
        """
        Appearance of the frame border.

        :return: The shadow type use by the frame
        :rtype: GLXCurses.GLXC.ShadowType
        """
        return self.__shadow_type

    @shadow_type.setter
    def shadow_type(self, shadow_type=None):
        """
        Set the ``shadow_type`` property value

        If set to ``None`` restore the ``GLXCurses.GLXC.SHADOW_NONE`` default value

        :param shadow_type: The shadow type use by the frame
        :type shadow_type: GLXCurses.GLXC.ShadowType
        :raise TypeError: when ``shadow_type`` is not a GLXCurses.GLXC.ShadowType
        """
        if shadow_type is None:
            shadow_type = GLXCurses.GLXC.SHADOW_NONE
        if shadow_type not in GLXCurses.GLXC.ShadowType:
            raise TypeError("'shadow_type' must be a valid GLXCurses.GLXC.ShadowType")
        if self.shadow_type != shadow_type:
            self.__shadow_type = shadow_type

    def new(self, label=None):
        """
        Create a new :class:`Frame <GLXCurses.Frame.Frame>`, with optional label text .

        If label is None, the label is omitted.

        :param label: the text to use as the label of the frame.
        :type label: str or None
        :return: a new :class:`Frame <GLXCurses.Frame.Frame>` widget
        :rtype: :class:`Widget <GLXCurses.Frame.Frame>`
        """
        self.__init__()
        self.label = label

        return self

    def set_label(self, label):
        """
        Sets the text of the label.

        If label is ``None``, the current label is removed.

        :param label: the text to use as the label of the frame.
        :type label: str or None
        """
        self.label = label

    def set_label_widget(self, label_widget):
        """
        Sets the label widget for the frame. This is the widget that will appear embedded in the top edge of the
        frame as a title.

        :param label_widget: the new label widget
        :type label_widget: :class:`Widget <GLXCurses.Widget.Widget>`
        """
        self.label_widget = label_widget

    def set_label_align(self, xalign, yalign):
        """
        Sets the alignment of the frame widget’s label. The default values for a newly created frame are 0.0 and 0.5.

        :param xalign: The position of the label along the top edge of the widget. A value of 0.0 represents left \
        alignment; 1.0 represents right alignment.
        :param yalign: The y alignment of the label. A value of 0.0 aligns under the frame; 1.0 aligns above the \
        frame. If the values are exactly 0.0 or 1.0 the gap in the frame won’t be painted because the label will \
        be completely above or below the frame.
        :type xalign: float
        :type yalign: float
        """
        self.label_xalign = xalign
        self.label_yalign = yalign

    def set_shadow_type(self, shadow_type=None):
        """
        Sets the shadow type for frame .

        :param shadow_type: the new :py:__area_data:`ShadowType`
        """
        self.shadow_type = shadow_type

    # The get_label() method returns the text in the label widget.
    # If there is no label widget or the label widget is not a Label the method returns None.
    def get_label(self):
        """
        If the frame’s label widget is a :class:`Label <GLXCurses.Label.Label>`, returns the text in the label widget. \
        (The frame will have a :class:`Label <GLXCurses.Label.Label>` for the label widget if \
        a non-NULL argument was passed when create the  :class:`Frame <GLXCurses.Frame.Frame>` .)

        :return: the text in the label, or :py:__area_data:`None` if there was no label widget or the label widget was \
        not a \
        :class:`Label <GLXCurses.Label.Label>` . This string is owned by GLXCurses and must not be modified or freed.
        :rtype: str or None
        """
        return self.label

    def get_label_align(self):
        """
        Retrieves the X and Y alignment of the frame’s label.

        .. seealso:: :func:`Frame.set_label_align() <GLXCurses.Frame.Frame.set_label_align()>`

        **xalign**: X location of frame label

        **yalign**: Y location of frame label


        :return: xalign, yalign
        :rtype: float,  float
        """
        return self.label_xalign, self.label_yalign

    def get_label_widget(self):
        """
        Retrieves the label widget for the frame.

        .. seealso:: :func:`Frame.set_label_widget() <GLXCurses.Frame.Frame.set_label_widget()>`

        :return: the label widget, or NULL if there is none.
        :rtype: :class:`Widget <GLXCurses.Widget.Widget>` or :py:__area_data:`None`
        """
        return self.label_widget

    def get_shadow_type(self):
        """
        Retrieves the shadow type of the frame.

        .. seealso:: :func:`Frame.set_shadow_type() <GLXCurses.Frame.Frame.set_shadow_type()>`

        :return: the current shadow type of the frame.
        :rtype: ShadowType
        """
        return self.shadow_type

    def draw_widget_in_area(self):
        self.draw_background(color=self.color_normal)
        if self.get_decorated():
            self._draw_box()

        # Draw the child.
        if self.child is not None:
            # Injection
            self.child.widget.stdscr = GLXCurses.Application().stdscr

            # self.get_child().set_subwin(self.get_subwin())
            self.child.widget.style = self.style

            if self.get_decorated():
                if self.child.widget.x != self.x + 1:
                    self.child.widget.x = self.x + 1
                if self.child.widget.y != self.y + 1:
                    self.child.widget.y = self.y + 1
                if self.child.widget.width != self.width - 2:
                    self.child.widget.width = self.width - 2
                if self.child.widget.height != self.height - 2:
                    self.child.widget.height = self.height - 2
            else:
                if self.child.widget.x != self.x:
                    self.child.widget.x = self.x
                if self.child.widget.y != self.y:
                    self.child.widget.y = self.y
                if self.child.widget.width != self.width:
                    self.child.widget.width = self.width
                if self.child.widget.height != self.height:
                    self.child.widget.height = self.height

            self.child.widget.draw()

        # Add the Label
        if self.label_widget:
            self.label_widget.stdscr = GLXCurses.Application().stdscr
            self.label_widget.y = self.y
            self.label_widget.x = self.x + 1
            self.label_widget.width = self.width - 2
            self.label_widget.height = 1
            self.label_widget.xalign = self.label_xalign
            self.label_widget.yalign = self.label_yalign
            self.label_widget.draw()
