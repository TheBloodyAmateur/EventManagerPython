import ipaddress
import re

from EventManager.processors.Processor import Processor


class MaskIPV4Address(Processor):
    __ip_address_ranges: list

    def __init__(self, ip_address_ranges: list):
        """
        Initializes the MaskIPV4Address processor with a list of IP address ranges to mask.

        :param ip_address_ranges: A list of IP address ranges to mask.
        """
        self.__ip_address_ranges = ip_address_ranges

    def process_kv(self, event: str) -> str:
        return self.__mask_ip_in_event(event, "ip=\"(\\d+\\.\\d+\\.\\d+\\.\\d+)\"")

    def process_json(self, event: str) -> str:
        return self.__mask_ip_in_event(event, "\"ip\":\\s+\"(\\d+\\.\\d+\\.\\d+\\.\\d+)\"")

    def process_xml(self, event: str) -> str:
        return self.__mask_ip_in_event(event, "<ip>(\\d+\\.\\d+\\.\\d+\\.\\d+)</ip>")

    def __mask_ip_in_event(self, event: str, regex: str) -> str:
        """
        Masks the IP address in the given event string based on the provided regex pattern.

        :param event: The event string containing the IP address.
        :param regex: The regex pattern to match the IP address.
        :return: The event string with the IP address masked.
        """
        # Implement the logic to mask the IP address using the regex pattern
        pattern = re.compile(regex)

        def mask_match(match):
            ip = match.group(1)
            if self.__is_ip_in_any_cidr_range(ip):
                return match.group(0).replace(ip, "***.***.***.***")
            return match.group(0)

        return pattern.sub(mask_match, event)

    def __is_ip_in_any_cidr_range(self, ip: str) -> bool:
        for cidr in self.__ip_address_ranges:
            if self._is_ip_in_cidr(ip, cidr):
                return True
        return False

    def _is_ip_in_cidr(self, ip: str, cidr: str) -> bool:
        try:
            return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr, strict=False)
        except ValueError:
            return False