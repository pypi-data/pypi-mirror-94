class RunningProperty(object):
    debug: bool

    def __init__(self) -> None:

        self.__running = False

        # self.running = None

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, value):
        """
        Set the is_running attribute

        :param value: False or True
        :type value: Boolean
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError("'running' property value must be bool type or None")
        if self.running != value:
            self.__running = value
