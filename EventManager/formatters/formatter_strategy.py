from abc import ABC, abstractmethod
from typing import Dict

from EventManager.formatters.key_value_wrapper import KeyValueWrapper


class FormatterStrategy(ABC):
    """
    The FormatterStrategy class is an abstract base class that defines the interface for formatting event logs.
    """

    @abstractmethod
    def format(self, metadata: Dict[str, str], *args: KeyValueWrapper) -> str:
        pass

    @abstractmethod
    def format_message(self, metadata: Dict[str, str], message: str) -> str:
        pass

    @abstractmethod
    def format_element(self, arg: KeyValueWrapper) -> str:
        pass

    @abstractmethod
    def format_arguments(self, body: str, *args: KeyValueWrapper) -> str:
        pass