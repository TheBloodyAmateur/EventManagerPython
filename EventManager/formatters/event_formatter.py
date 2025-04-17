from enum import Enum
from typing import Dict

from EventManager.formatters.csv_formatter import CsvFormatter
from EventManager.formatters.default_formatter import DefaultFormatter
from EventManager.formatters.json_formatter import JsonFormatter
from EventManager.formatters.key_value_formatter import KeyValueFormatter
from EventManager.formatters.key_value_wrapper import KeyValueWrapper
from EventManager.formatters.xml_formatter import XmlFormatter


class EventFormatter(Enum):
    DEFAULT = DefaultFormatter()
    KEY_VALUE = KeyValueFormatter()
    CSV = CsvFormatter()
    XML = XmlFormatter()
    JSON = JsonFormatter()

    def format(self, metadata: Dict[str, str], *args: KeyValueWrapper) -> str:
        return self.value.format(metadata, *args)

    def format_message(self, metadata: Dict[str, str], message: str) -> str:
        return self.value.format_message(metadata, message)

    def format_element(self, arg: KeyValueWrapper) -> str:
        return self.value.format_element(arg)

    def format_arguments(self, body: str, *args: KeyValueWrapper) -> str:
        return self.value.format_arguments(body, *args)