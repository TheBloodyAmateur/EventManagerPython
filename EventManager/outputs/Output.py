from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from EventManager.filehandlers.log_handler import LogHandler
    from EventManager.internal_event_manager import InternalEventManager



class Output():

    @abstractmethod
    def write(self, loghandler: 'LogHandler', event:str):
        """
        Abstract method to write an event to the output.
        :param loghandler: LogHandler instance to handle logging.
        :param event: The event to be written.
        """
        pass

    @abstractmethod
    def write(self, internal_event_manager: 'InternalEventManager', event:str):
        """
        Abstract method to write an event to the output.
        :param internal_event_manager: InternalEventManager instance to handle logging.
        :param event: The event to be written.
        """
        pass