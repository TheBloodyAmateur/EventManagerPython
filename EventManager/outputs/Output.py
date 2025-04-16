from abc import abstractmethod

from EventManager import InternalEventManager


class Output():

    @abstractmethod
    def write(self, loghandler:LogHandler, event:str):
        """
        Abstract method to write an event to the output.
        :param loghandler: LogHandler instance to handle logging.
        :param event: The event to be written.
        """
        pass

    @abstractmethod
    def write(self, internal_event_manager: InternalEventManager, event:str):
        """
        Abstract method to write an event to the output.
        :param internal_event_manager: InternalEventManager instance to handle logging.
        :param event: The event to be written.
        """
        pass