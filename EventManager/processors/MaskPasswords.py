import re

from EventManager.processors.Processor import Processor


class MaskPasswords(Processor):
    """
    The MaskPasswords class implements the Processor interface and provides functionality to mask passwords in events.
    """

    def process_kv(self, event: str) -> str:
        """
        Masks passwords in key-value formatted event data.
        """
        return re.sub(r'password="\w+"', 'password="***"', event)

    def process_json(self, event: str) -> str:
        """
        Masks passwords in JSON formatted event data.
        """
        return re.sub(r'"password":\s*"\w+"', '"password": "***"', event)

    def process_xml(self, event: str) -> str:
        """
        Masks passwords in XML formatted event data.
        """
        return re.sub(r'<password>\w+</password>', '<password>***</password>', event)
