import os

from EventManager.processors.Processor import Processor
import socket
import psutil


class EnrichingProcessor(Processor):
    __enriching_fields: list = ["hostname", "ip"]
    __enrichments: dict = {}

    def __init__(self, enriching_fields: list):
        """
        Initialize the EnrichingProcessor with a dictionary of enrichments.
        :param enriching_fields: Dictionary containing enrichment data.
        """
        self.__enriching_fields = enriching_fields if enriching_fields is not None else ["hostname", "ip"]
        self.__enrichments = {
            "hostname": self.__get_hostname(),
            "ip": self.__get_ip_address(),
            "osName": self.__get_os(),
            "osVersion": self.__get_os_version(),
            "javaVersion": self.__get_java_version(),
            "userName": self.__get_user_name(),
            "availableProcessors": self.__get_available_processors(),
            "freeMemory": self.__get_free_memory(),
            "totalMemory": self.__get_total_memory(),
        }

    def process_kv(self, event: str) -> str:
        return self.__enrich_kv_event(event)

    def process_json(self, event: str) -> str:
        return self.__enrich_json_event(event)

    def process_xml(self, event: str) -> str:
        return self.__enrich_xml_event(event)

    def __enrich_kv_event(self, event):
        builder = [event]
        for field in self.__enriching_fields:
            builder.append(f'{field}="{self.__get_value(field)}" ')
        return ''.join(builder)

    def __enrich_json_event(self, event):
        builder = [event[:-1], ","]
        for field in self.__enriching_fields:
            builder.append(f'"{field}":"{self.__get_value(field)}",')
        builder[-1] = builder[-1][:-1]  # Remove the trailing comma
        builder.append("}")
        return ''.join(builder)

    def __enrich_xml_event(self, event):
        builder = [event[:-8]]
        for field in self.__enriching_fields:
            builder.append(f'<{field}>{self.__get_value(field)}</{field}>')
        builder.append("</event>")
        return ''.join(builder)

    def __get_value(self, field: str) -> str:
        """
        Get the value of a specific field.
        :param field: The field name to retrieve the value for.
        :return: The value of the field as a string.
        """
        if field in self.__enrichments:
            return self.__enrichments[field]
        else:
            raise ValueError(f"Field {field} not found in enrichments.")

    def __get_hostname(self) -> str:
        """
        Get the hostname of the machine.
        :return: Hostname as a string.
        """
        return socket.gethostname()

    def __get_ip_address(self) -> str:
        """
        Get the IP address of the machine.
        :return: IP address as a string.
        """
        return socket.gethostbyname(socket.gethostname())

    def __get_os(self) -> str:
        """
        Get the operating system name.
        :return: Operating system name as a string.
        """
        return os.name

    def __get_os_version(self) -> str:
        """
        Get the operating system version.
        :return: Operating system version as a string.
        """
        return os.uname().version

    def __get_java_version(self) -> str:
        """
        Get the Java version.
        :return: Java version as a string.
        """
        return os.popen("java -version").read().strip()

    def __get_user_name(self) -> str:
        """
        Get the username of the current user.
        :return: Username as a string.
        """
        return os.getlogin()

    def __get_available_processors(self) -> int:
        """
        Get the number of available processors.
        :return: Number of available processors as an integer.
        """
        return os.cpu_count()

    def __get_free_memory(self) -> int:
        """
        Get the amount of free memory.
        :return: Free memory in bytes as an integer.
        """
        return psutil.virtual_memory().available

    def __get_total_memory(self) -> int:
        """
        Get the total memory.
        :return: Total memory in bytes as an integer.
        """
        return psutil.virtual_memory().total
