from glxeveloop.timer import Timer


class TimerProperty(object):
    def __init__(self) -> None:

        self.__timer = Timer()
        # self.timer = None

    @property
    def timer(self):
        return self.__timer

    @timer.setter
    def timer(self, value):
        if value is None:
            value = Timer()
        if not isinstance(value, Timer):
            raise TypeError("'timer' property value must be a Timer instance or None")
        if self.timer != value:
            self.__timer = value
