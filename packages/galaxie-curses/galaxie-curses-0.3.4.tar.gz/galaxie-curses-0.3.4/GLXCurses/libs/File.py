#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import os


class File(object):
    def __init__(self):
        self.__path = None
        self.__directory = None
        self.__name = None
        self.__extension = None
        self.__overwrite = None

        self.extension = None
        self.name = None
        self.directory = None
        self.path = None
        self.overwrite = None

    @property
    def extension(self):
        return self.__extension

    @extension.setter
    def extension(self, value=None):
        """
        Set the ``extension`` property value

        :param value: The extension of the file
        :type value: str or None
        :raise TypeError: When ``extension`` value is not a str type or None
        """
        if value is not None and type(value) != tuple and type(value) != str:
            raise TypeError('"extension" value must be a str type or None')
        if value is None:
            if self.extension is not None:
                self.__extension = None
        if value is not None and self.extension != value:
            self.__extension = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value=None):
        """
        Set the name property value

        :param value: The name of the file
        :type value: str or None
        :raise TypeError: When ``name`` value is not a str type or None
        """
        if value is not None and type(value) != str:
            raise TypeError('"name" value must be a str type or None')
        if value is None:
            if self.name is not None:
                self.__name = None
        if value is not None and self.name != value:
            self.__name = value

    @property
    def directory(self):
        return self.__directory

    @directory.setter
    def directory(self, value=None):
        """
        Set the directory property value

        :param value: The path of the file
        :type value: str or None
        :raise TypeError: When ``directory`` value is not a str type or None
        """
        if value is not None and type(value) != str:
            raise TypeError('"directory" value must be a str type or None')
        if value is None:
            if self.directory is not None:
                self.__directory = None
        if value is not None and self.directory != value:
            self.__directory = value

    @property
    def path(self):
        if self.directory is not None and self.name is not None:
            if self.extension:
                return os.path.join(
                    self.directory, "{0}{1}".format(self.name, self.extension)
                )
            else:
                return os.path.join(self.directory, self.name)
        else:
            return None

    @path.setter
    def path(self, value=None):
        """
        Set the path property value

        :param value: The path of the file
        :type value: str or None
        :raise TypeError: When value is not a str type or None
        """
        if value is not None and type(value) != str:
            raise TypeError('"path" value must be a str type or None')

        self.extension = None
        self.name = None
        self.directory = None
        self.__path = None

        if value is not None:

            # Filename isolation
            if os.path.basename(value).startswith("."):
                self.name = ".{0}".format(os.path.basename(value)[1:].split(".")[0])
            else:
                self.name = os.path.basename(value).split(".")[0]

            # Extension and post process
            spilt = os.path.basename(value).split(".")
            if spilt[0] == "":
                spilt.pop(0)

            if len(spilt) >= 1:
                spilt.pop(0)
                if ".".join(spilt) != "":
                    self.extension = ".{0}".format(".".join(spilt))

            # Directory
            self.directory = os.path.dirname(value)

    @property
    def overwrite(self):
        return self.__overwrite

    @overwrite.setter
    def overwrite(self, value=None):
        """
        Set the overwrite property value

        :param value: If the file can be overwrite
        :type value: bool or None
        :raise TypeError: When value is not a bool type or None
        """
        if value is None:
            if self.overwrite is not False:
                self.__overwrite = False
        else:
            if type(value) != bool:
                raise TypeError("'overwrite' value must be a bool type or None")
            if self.overwrite != value:
                self.__overwrite = value

    def is_binary(self):
        if os.path.exists(os.path.realpath(self.path)):
            if os.path.isfile(self.path) or os.path.islink(os.path.realpath(self.path)):
                fin = open(os.path.realpath(self.path), "rb")
                try:
                    chunk_size = 1024
                    while 1:
                        chunk = fin.read(chunk_size)
                        if b"\0" in chunk:
                            return True
                        if len(chunk) < chunk_size:
                            break
                finally:
                    fin.close()

                return False

        else:
            raise FileNotFoundError("File Not Found")

    def is_text(self):
        if os.path.exists(os.path.realpath(self.path)):
            if os.path.isfile(self.path) or os.path.islink(os.path.realpath(self.path)):
                fin = open(os.path.realpath(self.path), "rb")
                try:
                    chunk_size = 1024
                    while 1:
                        chunk = fin.read(chunk_size)
                        if b"\0" in chunk:
                            return False
                        if len(chunk) < chunk_size:
                            break
                finally:
                    fin.close()

                return True

        else:
            raise FileNotFoundError("File Not Found")

    def found_best_output_file_name(self):
        output_file = None
        if os.path.exists(self.path):
            if self.overwrite:
                output_file = self.path
            else:
                i = 1
                if self.extension:
                    extension = self.extension
                else:
                    extension = ""
                while os.path.exists(
                    os.path.join(
                        self.directory, "{0}-{1}{2}".format(self.name, i, extension)
                    )
                ):
                    i += 1
                output_file = os.path.join(
                    self.directory, "{0}-{1}{2}".format(self.name, i, extension)
                )

        return output_file
