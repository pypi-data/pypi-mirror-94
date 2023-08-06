from glxeveloop.hooks import Hooks
from glxeveloop.timer import Timer
import logging
import sys


class Start(object):
    running: bool
    debug: bool
    timer: Timer
    hooks: Hooks

    def start(self) -> None:
        """
        Runs a Loop until ``Mainloop.stop()`` is called on the loop. If this is called for the thread of the loop's
        , it will process queue from the loop, otherwise it will simply wait.
        """
        if hasattr(self, "debug") and self.debug:
            logging.debug("Starting " + self.__class__.__name__)
        self.running = True

        # Normally it the first refresh of the application, it can be considered as the first stdscr display.
        # Consider a chance to crash before the start of the loop
        try:
            if hasattr(self, "sequence") and self.sequence:
                self.sequence()

        except Exception:
            if hasattr(self, "stop") and self.stop:
                self.stop()
            sys.stdout.write("{0}\n".format(sys.exc_info()[0]))
            sys.stdout.flush()
            raise

        # A bit light for notify about we are up and running, but we are really inside the main while(1) loop
        if hasattr(self, "debug") and self.debug:
            logging.debug(self.__class__.__name__ + ": Started")
        # The loop
        while self.running:

            try:
                if hasattr(self.hooks, "statement") and self.hooks.statement:
                    self.hooks.statement()

                if hasattr(self, "sequence") and self.sequence:
                    self.sequence()

                try:
                    if hasattr(self.timer, "tick") and self.timer.tick:
                        self.timer.tick()
                except TypeError:  # pragma: no cover
                    pass

            except KeyboardInterrupt:  # pragma: no cover
                if (
                        hasattr(self.hooks, "keyboard_interruption")
                        and self.hooks.keyboard_interruption
                ):
                    self.hooks.keyboard_interruption()
                else:
                    if hasattr(self, "stop") and self.stop:
                        self.stop()

            except Exception:  # pragma: no cover
                if hasattr(self, "stop") and self.stop:
                    self.stop()
                sys.stdout.write("{0}\n".format(sys.exc_info()[0]))
                sys.stdout.flush()
                raise

        if hasattr(self.hooks, "finalization") and self.hooks.finalization:

            if hasattr(self, "debug") and self.debug:
                logging.debug(self.__class__.__name__ + ": Call finalization method")

            self.hooks.finalization()

        if hasattr(self, "debug") and self.debug:
            logging.debug(self.__class__.__name__ + ": All operations is stop")
