#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import GLXCurses


class FileChooserMenu(GLXCurses.Container, GLXCurses.Movable):
    def __init__(self, parent=None, y=None, x=None, label=None):
        """

        :param parent:
        :type parent: Filechooser
        :param y:
        :param x:
        :param label:
        """
        GLXCurses.Container.__init__(self)
        GLXCurses.Movable.__init__(self)

        self.__history_box_num_cols = None
        self.__history_dir_list = None
        self.__label = None

        self.history_box_num_cols = None
        self.history_dir_list = None
        self.label = " {0} ".format(label)

        # self.y_parent, self.x_parent = self.stdscr.getbegyx()
        # self.y_parent = self.parent.y
        # self.x_parent = self.parent.x
        # self.y_max_parent, self.x_max_parent = parent.stdscr.getmaxyx()
        self.y = y
        self.x = x

        self.width = len(str(label))

        self.history_dir_list = []

    def draw_widget_in_area(self):
        self.update_size()


        # # Inside the history menu
        # self.draw_background(parent.style.color(
        #         fg=parent.style.get_attributes_rgb_color("dark", "STATE_NORMAL"),
        #         bg=parent.style.get_attributes_rgb_color("white", "STATE_NORMAL"),
        #     ))

        # history_box_num_lines, history_box_num_cols = history_box.getmaxyx()
        # history_box_num_lines = self.height
        # history_box_num_cols = self.width
        # max_cols_to_display = history_box_num_cols - 2
        # max_lines_to_display = 1

        # for I in range(0, history_box_num_lines - 2):
        #     history_box.addstr(
        #         I + 1,
        #         1,
        #         str(" " * int(history_box_num_cols - 2)),
        #         parent.style.color(
        #             fg=parent.style.get_attributes_rgb_color("dark", "STATE_NORMAL"),
        #             bg=parent.style.get_attributes_rgb_color("white", "STATE_NORMAL"),
        #         ),
        #     )
        #     max_lines_to_display += 1
        # parent.history_menu_can_be_display = max_lines_to_display
        #
        # for I in range(
        #         0 + parent.history_menu_item_list_scroll, parent.history_menu_can_be_display
        # ):
        #     if I < len(parent.history_dir_list):
        #
        #         if parent.history_menu_selected_item == I:
        #             parent.history_menu_selected_item_value = parent.history_dir_list[I]
        #             if len(str(parent.history_dir_list[I])) >= max_cols_to_display:
        #                 history_box.addstr(
        #                     I + 1,
        #                     1,
        #                     str(parent.history_dir_list[I][:max_cols_to_display]),
        #                     parent.style.color(
        #                         fg=parent.style.get_attributes_rgb_color("dark", "STATE_NORMAL"),
        #                         bg=parent.style.get_attributes_rgb_color("bg", "STATE_SELECTED"),
        #                     ),
        #                 )
        #             else:
        #                 history_box.addstr(
        #                     I + 1,
        #                     1,
        #                     str(parent.history_dir_list[I]),
        #                     parent.style.color(
        #                         fg=parent.style.get_attributes_rgb_color("dark", "STATE_NORMAL"),
        #                         bg=parent.style.get_attributes_rgb_color("bg", "STATE_SELECTED"),
        #                     ),
        #                 )
        #                 history_box.addstr(
        #                     I + 1,
        #                     len(str(parent.history_dir_list[I])) + 1,
        #                     str(
        #                         " "
        #                         * int(
        #                             history_box_num_cols
        #                             - 2
        #                             - len(str(parent.history_dir_list[I]))
        #                         )
        #                     ),
        #                     parent.style.color(
        #                         fg=parent.style.get_attributes_rgb_color("dark", "STATE_NORMAL"),
        #                         bg=parent.style.get_attributes_rgb_color("bg", "STATE_SELECTED"),
        #                     ),
        #                 )
        #         else:
        #             if len(str(parent.history_dir_list[I])) >= max_cols_to_display:
        #                 history_box.addstr(
        #                     I + 1,
        #                     1,
        #                     str(parent.history_dir_list[I][:max_cols_to_display]),
        #                     parent.style.color(
        #                         fg=parent.style.get_attributes_rgb_color("dark", "STATE_NORMAL"),
        #                         bg=parent.style.get_attributes_rgb_color("white", "STATE_NORMAL"),
        #                     ),
        #                 )
        #             else:
        #                 history_box.addstr(
        #                     I + 1,
        #                     1,
        #                     str(parent.history_dir_list[I]),
        #                     parent.style.color(
        #                         fg=parent.style.get_attributes_rgb_color("dark", "STATE_NORMAL"),
        #                         bg=parent.style.get_attributes_rgb_color("white", "STATE_NORMAL"),
        #                     ),
        #                 )
        #
        # history_box.box()
        if self.label:
            self.draw_titles()

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value=None):
        if value is None:
            self.__label = None
            return
        if type(value) != str:
            raise TypeError("'label' property value must be str type or None")
        if self.label != value:
            self.__label = value

    @property
    def history_box_num_cols(self):
        return self.__history_box_num_cols

    @history_box_num_cols.setter
    def history_box_num_cols(self, value=None):
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError("'history_box_num_cols' property value must be int type or None")
        if self.history_box_num_cols != value:
            self.__history_box_num_cols = value

    @property
    def history_dir_list(self):
        return self.__history_dir_list

    @history_dir_list.setter
    def history_dir_list(self, value=None):
        if value is None:
            value = []
        if type(value) != list:
            raise TypeError("'history_dir_list' property value must be a list type or None")
        if self.history_dir_list != value:
            self.__history_dir_list = value

    def draw_titles(self):
        # # Title
        self.add_string(
            y=0,
            x=(int(self.history_box_num_cols / 2)) - int((len(self.label) / 2)),
            text=self.label,
            color=self.style.color(
                fg=self.style.attribute_to_rgb("dark", "STATE_NORMAL"),
                bg=self.style.attribute_to_rgb("white", "STATE_NORMAL")
            )
        )

    def update_size(self):
        self.width = None
        self.height = None
        self.preferred_width = None
        self.preferred_height = None

        # Look for history window size it depend of the history list
        if len(self.parent.history_dir_list) + 2 < self.y_max_parent:
            history_y = len(parent.history_dir_list) + 2

        else:
            history_y = self.y_max_parent - 1

        if len(parent.history_dir_list) > 0:
            history_x = len(max(parent.history_dir_list, key=len)) + 2
            if history_x > self.x_max_parent - 1:
                history_x = self.x_max_parent
        else:
            history_x = len(self.label) + 2

        # history_box = self.subwin(history_y, history_x, 2, 0)
        self.y = history_y
        self.x = history_x
        self.width = 2
        self.width = 0


    # def mouse_clicked(self, mouse_event):
    #     (event_id, x, y, z, event) = mouse_event
    #     if self.y_parent <= y <= self.y_parent + 1:
    #         if self.x + self.x_parent <= x < self.x + self.x_parent + self.Width:
    #             return 1
    #     else:
    #         return 0
