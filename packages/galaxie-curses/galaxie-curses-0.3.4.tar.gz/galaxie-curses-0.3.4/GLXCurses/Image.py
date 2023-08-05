#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import PIL
import GLXCurses


class Image(GLXCurses.Misc, GLXCurses.File, GLXCurses.Colors):
    def __init__(self):
        GLXCurses.Misc.__init__(self)
        GLXCurses.File.__init__(self)
        GLXCurses.Colors.__init__(self)

        self.glxc_type = "GLXCurses.Image"
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        self.__data = None
        self.__image_object = None
        self.__original_image_object = None
        self.__is_resized = None
        self.__height_original = None
        self.__height_max = None
        self.__hsp_debug = None
        self.__width_original = None
        self.__width_max = None

        self.data = None
        self.image_object = None
        self.image_original = None
        self.original_image_object = None
        self.is_resized = None
        self.height_max = None
        self.height_original = None
        self.width_max = None
        self.width_original = None
        self.hsp_debug = None

        self.bg_color = (255, 255, 255)

        self.debug = True

        self.chars = '░▒▓█'
        self.width_zoom = 1
        self.height_zoom = 2

    @property
    def image_object(self):
        """
        Store the modified image

        :return:
        """
        return self.__image_object

    @image_object.setter
    def image_object(self, value=None):
        if value is None:
            self.__image_object = None
            return
        if self.image_object != value:
            self.__image_object = value

    @property
    def data(self):
        """
        Get ``data`` property

        :return: image data as a list
        :rtype: list
        """
        return self.__data

    @data.setter
    def data(self, value=None):
        """
        Set ``data`` property

        :param value: a list
        :type value: list or None
        """
        if value is None:
            value = []
        if type(value) != list:
            raise TypeError("'data' property value must be a list type or None")
        if self.data != value:
            self.__data = value

    @property
    def hsp_debug(self):
        """
        Get ``hsp_debug`` property

        :return: image hsp_debug as a list
        :rtype: list
        """
        return self.__hsp_debug

    @hsp_debug.setter
    def hsp_debug(self, value=None):
        """
        Set ``hsp_debug`` property

        :param value: a list
        :type value: list or None
        """
        if value is None:
            value = []
        if type(value) != list:
            raise TypeError("'hsp_debug' property value must be a list type or None")
        if self.hsp_debug != value:
            self.__hsp_debug = value

    @property
    def width_max(self):
        """
        Get the ``width_max`` property value

        :return: ``width_max`` property value
        :rtype: int or None
        """
        return self.__width_max

    @width_max.setter
    def width_max(self, value=None):
        """
        Set the ``width_max`` property value

        Default value is 80 and be restore when ``width_max`` property value is set to None

        :param value: Image width_max is pixels
        :type value: int or None
        :raise TypeError: when ``width_max`` property value is not a int type or None
        """
        if value is None:
            value = 80
        if type(value) != int:
            raise TypeError('"width_max" value must be a int or None')
        if self.width_max != value:
            self.__width_max = value

    @property
    def width_original(self):
        """
        Get the ``width_original`` property value

        :return: ``width_original`` property value
        :rtype: int or None
        """
        return self.__width_original

    @width_original.setter
    def width_original(self, value=None):
        """
        Set the ``width_original`` property value

        Default value is 80 and be restore when ``width_original`` property value is set to None

        :param value: Image width_original in pixels
        :type value: int or None
        :raise TypeError: when ``width_original`` property value is not a int type or None
        """
        if value is None:
            value = 80
        if type(value) != int:
            raise TypeError('"width_original" value must be a int or None')
        if self.width_original != value:
            self.__width_original = value

    @property
    def height_max(self):
        """
        Get the ``height_max`` property value

        :return: ``height_max`` property value
        :rtype: int or None
        """
        return self.__height_max

    @height_max.setter
    def height_max(self, value=None):
        """
        Set the ``height_max`` property value

        Default value is 20 and be restore when ``height_max`` property value is set to None

        :param value: Image height is pixels
        :type value: int or None
        :raise TypeError: when ``height_max`` property value is not a int type or None
        """
        if value is None:
            value = 20
        if type(value) != int:
            raise TypeError('"height_max" value must be a int or None')
        if self.height_max != value:
            self.__height_max = value

    @property
    def height_original(self):
        """
        Get the ``height_original`` property value

        it property is use when the widget discover image size

        :return: ``height_original`` property value
        :rtype: int or None
        """
        return self.__height_original

    @height_original.setter
    def height_original(self, value=None):
        """
        Set the ``height_original`` property value

        Default value is 20 and be restore when ``height_original`` property value is set to None

        :param value: Image height in pixels
        :type value: int or None
        :raise TypeError: when ``height_original`` property value is not a int type or None
        """
        if value is None:
            value = 20
        if type(value) != int:
            raise TypeError('"height_original" value must be a int or None')
        if self.height_original != value:
            self.__height_original = value

    @property
    def is_resized(self):
        """
        Whether the image will be resized directly on the widget.

        :return: True or False
        :rtype: bool
        """
        return self.__is_resized

    @is_resized.setter
    def is_resized(self, value=None):
        """
        Set ``is_resized`` property

        :param value: if True image will be resized directly on the widget
        :type value: bool
        :raise TypeError: if ``is_resized`` is not a bool type or None
        """
        if value is None:
            value = False
        if not isinstance(value, bool):
            raise TypeError("'value' must be a bool type")
        if self.is_resized != value:
            self.__is_resized = value

    def load_image(self, path=None):
        if path is None:
            path = self.path

        fp = open(path, "rb")
        p = PIL.ImageFile.Parser()

        while 1:
            s = fp.read(1024)
            if not s:
                break
            p.feed(s)
        fp.close()

        self.original_image_object = p.close()

        self.image_object = self.original_image_object
        self.width_original, self.height_original = self.original_image_object.size

    def draw_widget_in_area(self):
        if self.data:
            for item in self.data:
                self.add_string(
                    y=item['y'],
                    x=item['x'],
                    text=item['char'],
                    color=item['color']
                )

    def to_data(self):
        self.data = None
        self.image_object = self.original_image_object
        try:

            self.image_object = self.image_object.resize((
                int(round(self.width_original * self.width_zoom)),
                int(round((self.height_original / self.height_zoom)))),
                resample=3
            )

            # Remove Transparency
            if (
                    self.image_object.mode in ("LA", "PA", "RGBa", "LA", "RGBA")
                    or (self.image_object.mode == "P" and "transparency" in self.image_object.info)
            ):
                self.image_object = self.image_object.convert("RGB")

            # Test if the image is RVB
            width, height = self.image_object.size

            if self.image_object.mode in ("1", "L"):
                for y in range(0, height):
                    for x in range(0, width):
                        light = self.image_object.getpixel((x, y))
                        self.data.append({
                            'x': x,
                            'y': y,
                            'char': '█',
                            'color': self.color(
                                fg=(light, light, light),
                                bg=(0, 0, 0)
                            )
                        })

            else:
                for y in range(0, height):
                    for x in range(0, width):
                        self.data.append({
                            'x': x,
                            'y': y,
                            'char': '█',
                            'color': self.color(
                                fg=(self.image_object.getpixel((x, y))),
                                bg=(0, 0, 0)
                            )
                        })


        except ValueError:
            pass
        except OverflowError:
            pass
