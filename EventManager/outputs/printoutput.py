from EventManager.outputs.Output import Output
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from EventManager.internal_event_manager import InternalEventManager
    from EventManager.filehandlers.log_handler import LogHandler


class PrintOutput(Output):
    """
    A class to handle print output for events.
    """

    def write(self, loghandler:'LogHandler', event: str):
        """
        Writes the event to the standard output.

        :param loghandler:
        :param event: The event to be written.
        """
        print(event)

    def write(self, internal_event_manager: 'InternalEventManager', event: str):
        """
        Writes the event to the standard output.

        :param internal_event_manager: InternalEventManager instance to handle logging.
        :param event: The event to be written.
        """
        print(event)