from abc import ABC, abstractmethod

class Processor(ABC):
    """
    The Processor interface provides methods to process events in different formats (KV, JSON, XML).
    """

    @abstractmethod
    def process_kv(self, event: str) -> str:
        """
        Processes a key-value formatted event.

        :param event: The key-value formatted event string.
        :return: The processed event string.
        """
        pass

    @abstractmethod
    def process_json(self, event: str) -> str:
        """
        Processes a JSON formatted event.

        :param event: The JSON formatted event string.
        :return: The processed event string.
        """
        pass

    @abstractmethod
    def process_xml(self, event: str) -> str:
        """
        Processes an XML formatted event.

        :param event: The XML formatted event string.
        :return: The processed event string.
        """
        pass