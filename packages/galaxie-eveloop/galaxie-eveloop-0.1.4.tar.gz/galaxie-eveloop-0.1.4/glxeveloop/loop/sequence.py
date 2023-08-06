from glxeveloop.hooks import Hooks


class SequenceLoop(object):
    hooks: Hooks

    def sequence(self) -> None:
        """
            * Parse user input into a Statement object
            * Start timer
            * Call precmd method
            * Add statement to History
            * Call cmd method
            * Call postcmd method
            * Stop timer and display the elapsed time
            * In Case of Exit call methods loop_finalization

        :return: Nothing
        :rtype: None
        """
        if self.hooks.pre:
            self.hooks.pre()

        if hasattr(self, "handle_event"):
            self.handle_event()

        if self.hooks.cmd:
            self.hooks.cmd()

        if self.hooks.post:
            self.hooks.post()
