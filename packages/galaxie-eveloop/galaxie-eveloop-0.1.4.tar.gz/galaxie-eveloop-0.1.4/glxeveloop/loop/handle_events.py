from glxeveloop.hooks import Hooks
from glxeveloop.timer import Timer
from threading import Thread
from queue import Queue
import logging
import sys


class HandleEvents(object):
    debug: bool
    hooks: Hooks
    queue: Queue

    def handle_event(self):
        event = None
        try:
            handler_list = []
            while not self.queue.empty():
                event = self.queue.get()
                if self.hooks.dispatch:
                    if hasattr(self, "debug") and self.debug:
                        logging.debug(
                            "{3}.handle_event ({0}, {1}) to {2}".format(
                                event[0],
                                event[1],
                                self.hooks.dispatch,
                                self.__class__.__name__,
                            )
                        )
                    handler_list.append(
                        Thread(target=self.hooks.dispatch(event[0], event[1]))
                    )

            for handler in handler_list:
                handler.start()
            for handler in handler_list:
                handler.join()

        except KeyError as the_error:  # pragma: no cover
            # Permit to have error logs about unknown event
            logging.error(
                "{0}._handle_event(): KeyError:{1} event:{2}".format(
                    self.__class__.__name__, the_error, event
                )
            )
