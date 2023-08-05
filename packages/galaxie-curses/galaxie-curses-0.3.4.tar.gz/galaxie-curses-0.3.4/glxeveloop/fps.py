class FPS(object):
    def __init__(self):
        """
        :Property's Details:

        .. py:data:: fps

           The number of Frames per second. (in **fps**)

           Note that not correspond exactly to a true movies or game FPS, it's similar but it's not.

           For the :class:`Timer <glxeveloop.timer.Timer>` Class, it correspond more about how many time **1 second**
           is divided.

           The ``value`` passed as argument to
           :func:`Timer.set_fps() <glxeveloop.timer.Timer.set_fps()>` method is clamped
           to lie between :py:data:`min` and :py:data:`fps_max`
           property's.

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 25.0                          |
              +---------------+-------------------------------+

        .. py:data:: min

           The min Frames number per second allowed before the :class:`Timer <glxeveloop.timer.Timer>` stop to apply
           a rate limit to the :py:data:`fps` property. (in **fps**)

           It can be considered as the min value of the CLAMP process

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 2.0                           |
              +---------------+-------------------------------+

        .. py:data:: fps_max

           The maximum Frames number per second allowed before the :class:`Timer <glxeveloop.timer.Timer>` start to rate
           limit the :py:data:`fps` property.

           It can be considered as the max value of the CLAMP process.

           By default it have no limit fps_max = float("inf")

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | float("inf")                  |
              +---------------+-------------------------------+

        .. py:data:: fps_increment

           The self-correcting timing algorithms will try to increase or decrease :py:data:`fps` property
           with the :py:data:`fps_increment` property value.

           Note: the :py:data:`fps_increment` property will be not clamped

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0.1                           |
              +---------------+-------------------------------+

        .. py:data:: fps_min_increment

           :py:data:`fps_min_increment` is the lower allowed increment value

           The self-correcting timing will try to adjust :py:data:`fps` property
           in range of :py:data:`fps_min_increment` to :py:data:`fps_max_increment`

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0.1                           |
              +---------------+-------------------------------+

        .. py:data:: fps_max_increment

           :py:data:`fps_max_increment` is the upper allowed increment value

           The self-correcting timing will try to adjust :py:data:`fps` property
           in range of :py:data:`fps_min_increment` to :py:data:`fps_max_increment`

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0.1                           |
              +---------------+-------------------------------+

        """
        self.__value = None
        self.__fps_increment = None
        self.__min = None
        self.__fps_min_increment = None
        self.__max = None
        self.__fps_max_increment = None

        self.min = None
        self.max = None
        self.value = None

        self.fps_min_increment = None
        self.fps_max_increment = None
        self.fps_increment = None

    @property
    def value(self):
        """
        The number of Frames per second. (in **fps**)

        Note that not correspond exactly to a true movies or game FPS, it's similar but it's not.

        For the :class:`Timer <glxeveloop.timer.Timer>` Class, it correspond more about how many time **1 second**
        is divided.

        .. note:: If set the value will be clamped between :py:data:`min` and :py:data:`fps_max` properties value.

        :return: :py:data:`fps` property value. (in **fps**)
        :rtype: float
        """
        return self.__value

    @value.setter
    def value(self, value=None):
        """
        Set the :class:`Timer <glxeveloop.timer.Timer>` :py:data:`fps` property.

        :param value: Frames number per second. (in **fps**)
        :type value: float
        :raise TypeError: if ``fps`` parameter is not a :py:data:`float` type
        """
        if value is None:
            value = 60.00
        if type(value) == int:
            value = float(value)
        if type(value) != float:
            raise TypeError("'value' property value must be float/int type or None")

        # CLAMP to the absolute value
        clamped_value = abs(max(min(self.max, value), self.min))

        if self.value != round(clamped_value, 2):
            self.__value = round(clamped_value, 2)

    @property
    def min(self):
        """
        Get the :class:`Timer <glxeveloop.timer.Timer>` :py:data:`min` property value.

        :return: :py:data:`min` property value. (in **fps**)
        :rtype: float
        """
        return self.__min

    @min.setter
    def min(self, value=None):
        """
        Set the :py:data:`min` property value.

        It correspond to a imposed minimal amount of frame rate

        :return: :py:data:`min` property value. (in **fps**)
        :rtype: float
        :raise TypeError: if ``min`` parameter is not a :py:data:`float` type
        """
        if value is None:
            value = 30.0

        if type(value) == int:
            value = float(value)

        if type(value) != float:
            raise TypeError("'min' property value must be float/int type or None")

        if self.min != value:
            self.__min = value

    @property
    def max(self):
        """
        Get the :class:`Timer <glxeveloop.timer.Timer>` :py:attr:`fps_max` property value.

        :return: :py:attr:`fps_max` property value. (in **fps**)
        :rtype: float
        """
        return self.__max

    @max.setter
    def max(self, value=None):
        """
        Set the :class:`Timer <glxeveloop.timer.Timer>` :py:attr:`fps_max` property value.

        It correspond to a imposed max amount of frame rate used during acceleration phase

        :param value: :py:attr:`fps_max` property value. (in **fps**)
        :type value: :py:obj:`float` or :py:data:`int` or :py:obj:`None`
        :raise TypeError: if ``max_fps`` parameter value is not a :py:data:`float` or
        :py:data:`int` type or :py:obj:`None`
        """
        if value is None:
            value = float("inf")

        if type(value) == int:
            value = float(value)

        if type(value) != float:
            raise TypeError("'max_fps' property value parameter must be a float or None")

        if self.max != value:
            self.__max = value

    @property
    def fps_increment(self):
        """
        Get the :class:`Timer <glxeveloop.timer.Timer>` :py:data:`fps_increment` property value.

        :return: :py:data:`fps_increment` property value. (in **fps**)
        :rtype: float
        """
        return self.__fps_increment

    @fps_increment.setter
    def fps_increment(self, fps_increment=0.1):
        """
        Set the :class:`Timer <glxeveloop.timer.Timer>` :py:attr:`fps_increment` property.

        The self-correcting timing algorithms will try to increase or decrease :py:attr:`fps_increment` property
        with it step increment.

        :param fps_increment: Frames number per second. (in **fps**)
        :type fps_increment: float
        :raise TypeError: if ``fps_increment`` parameter is not a :py:data:`float` type
        """
        if fps_increment is None:
            fps_increment = 1.0
        if type(fps_increment) != float:
            raise TypeError("'fps' parameter must be a float")
        if self.fps_increment != fps_increment:
            self.__fps_increment = fps_increment

    @property
    def fps_min_increment(self):
        """
        Get the smaller of step increment

        The :class:`Timer <glxeveloop.timer.Timer>` :py:data:`fps_min_increment` property value.

        See :func:`Timer.set_fps_min_increment() <glxeveloop.timer.Timer.set_fps_min_increment()>`
        for more information's

        :return: :py:data:`fps_min_increment` property value. (in **fps**)
        :rtype: float
        """
        return self.__fps_min_increment

    @fps_min_increment.setter
    def fps_min_increment(self, fps_min_increment=0.1):
        """
        Set the :class:`Timer <glxeveloop.timer.Timer>` :py:data:`fps_min_increment` increment.

        The algorithms will try to increase or decrease :py:data:`fps` property with
        :py:attr:`fps_increment` as step .

        For fast limit rate stabilization the :class:`Timer <glxeveloop.timer.Timer>` can use
        :py:data:`fps_min_increment`
        and :py:data:`fps_max_increment` property for make a gap in contain in a range, where
        :py:data:`fps_min_increment` will force a minimal amount of increment and
        :py:data:`fps_max_increment` will force a maximal amount of increment.

        :param fps_min_increment: Frames number per second. (in **fps**)
        :type fps_min_increment: float
        :raise TypeError: if ``fps_min_increment`` parameter is not a :py:data:`float` type
        """
        if fps_min_increment is None:
            fps_min_increment = 0.1
        if type(fps_min_increment) != float:
            raise TypeError("'fps_min_increment' parameter must be a float type")
        if self.fps_min_increment != fps_min_increment:
            self.__fps_min_increment = fps_min_increment

    @property
    def fps_max_increment(self):
        """
        Get the bigger of step increment

        Get the :class:`Timer <glxeveloop.timer.Timer>` :py:data:`fps_max_increment` property value.

        :return: :py:data:`fps_max_increment` property value. (in **fps**)
        :rtype: float
        """
        return self.__fps_max_increment

    @fps_max_increment.setter
    def fps_max_increment(self, fps_max_increment=None):
        """
        Set the :class:`Timer <glxeveloop.timer.Timer>` :py:data:`fps_max_increment` increment.

        The self-correcting timing algorithms will try to increase or decrease :py:data:`fps` property with
        :py:attr:`fps_increment` as step .

        For fast limit rate stabilization the :class:`Timer <glxeveloop.timer.Timer>` can use
        :py:data:`fps_min_increment`
        and :py:data:`fps_max_increment` for make gap in a increment range, where :py:data:`fps_max_increment` will
        fixe the limit .

        :param fps_max_increment: Frames number per second. (in **fps**)
        :type fps_max_increment: float
        :raise TypeError: if ``fps_max_increment`` parameter is not a :py:data:`float` type
        """
        if fps_max_increment is None:
            fps_max_increment = 100.0
        if type(fps_max_increment) != float:
            raise TypeError("'max_fps_increment' parameter must be a float")
        if self.fps_max_increment != fps_max_increment:
            self.__fps_max_increment = fps_max_increment
