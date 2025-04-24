import threading
import traceback
import socket

from EventManager.formatters.event_formatter import EventFormatter
import time


class EventCreator:
    """
    The EventCreator class is a builder class that creates event logs.
    Contrary to the EventFormatter class, it can create event logs with a custom format. The format can be specified by
    the user when creating an instance of the EventCreator class. The format can be one of the following: "json", "xml",
    "csv", or "key-value".

    The class includes information which can be found in the default format, such as the class name, method name, line
    number, timestamp, level, exception, message, and arguments. These values are generated when creating an instance of
    the EventCreator class, this should be kept in mind when creating events.
    """

    def __init__(self, format="key-value"):
        """
        The constructor of the EventCreator class.

        :param format: The format of the event log. The format can be one of the following: "json", "xml", "csv", or
                       "key-value". If the format is not one of the specified formats, the default format is "key-value".
        """

        self.__stack_trace_element: traceback.StackSummary = traceback.extract_stack()
        self.__class_name: str = self.__stack_trace_element[-2].name
        self.__method_name: str = self.__stack_trace_element[-2].name
        self.__line_number: int = self.__stack_trace_element[-2].lineno
        self.__event: str = ""
        self.__event_format: str
        self.__formatter: EventFormatter
        self.__format_separator: str = " "

        self.__event_format = format

        if format == "json":
            self.__event = "{"
            self.__formatter = EventFormatter.JSON
            self.__format_separator = ","
        elif format == "xml":
            self.__formatter = EventFormatter.XML
            self.__event = "<event>"
            self.__format_separator = ""
        elif format == "csv":
            self.__formatter = EventFormatter.CSV
            self.__format_separator = ","
        else:
            self.__event = ""
            self.__formatter = EventFormatter.KEY_VALUE
            self.__format_separator = " "

    def _append_element(self, key, value):
        """
        Appends a key-value pair to the event. In case the format is "csv", only the value is appended.

        :param key: The key.
        :param value: The value.
        """
        from EventManager.formatters import KeyValueWrapper

        self.__event += self.__formatter.format_element(KeyValueWrapper(key, value))

    def _append_arguments(self, *args):
        """
        Appends the arguments to the event log.

        :param args: The arguments to append.
        """
        self.__event += self.__formatter.format_arguments(self.__event, *args)

    def _append_separator(self):
        """
        Appends a separator to the event log.
        """
        if self.__format_separator is not None:
            self.__event += self.__format_separator

    def line_number(self) -> "EventCreator":
        """
        Appends the line number to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("line_number", str(self.__line_number))
        self._append_separator()
        return self

    def class_name(self) -> "EventCreator":
        """
        Appends the class name to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("class_name", self.__class_name)
        self._append_separator()
        return self

    def method_name(self) -> "EventCreator":
        """
        Appends the method name to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("method_name", self.__method_name)
        self._append_separator()
        return self

    def timestamp(self, timestamp_format: str) -> "EventCreator":
        """
        Appends the timestamp to the event log.

        :return: The EventCreator instance.
        """

        def is_valid_time_format(time_format: str) -> bool:
            if time_format is None or time_format.strip() == "":
                return False
            try:
                time.strftime(time_format)
                return True
            except ValueError:
                return False

        if is_valid_time_format(timestamp_format):
            self._append_element("timestamp", str(time.strftime(timestamp_format)))
        else:
            timestamp = str(time.strftime("%Y-%m-%d %H:%M:%S"))
            self._append_element("timestamp", timestamp)
        self._append_separator()
        return self

    def level(self, level: str) -> "EventCreator":
        """
        Appends the level to the event log.

        :param level: The level of the event log.
        :return: The EventCreator instance.
        """
        self._append_element("level", str(level))
        self._append_separator()
        return self

    def fatal_level(self) -> "EventCreator":
        """
        Appends the fatal level to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("level", "FATAL")
        self._append_separator()
        return self

    def error_level(self) -> "EventCreator":
        """
        Appends the error level to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("level", "ERROR")
        self._append_separator()
        return self

    def warning_level(self) -> "EventCreator":
        """
        Appends the warning level to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("level", "WARNING")
        self._append_separator()
        return self

    def info_level(self) -> "EventCreator":
        """
        Appends the info level to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("level", "INFO")
        self._append_separator()
        return self

    def debug_level(self) -> "EventCreator":
        """
        Appends the debug level to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("level", "DEBUG")
        self._append_separator()
        return self

    def exception(self, exception: Exception) -> "EventCreator":
        """
        Appends the exception to the event log.

        :param exception: The exception to append.
        :return: The EventCreator instance.
        """
        self._append_element("exception", str(exception))
        self._append_separator()
        return self

    def message(self, message: str) -> "EventCreator":
        """
        Appends the message to the event log.

        :param message: The message to append.
        :return: The EventCreator instance.
        """
        self._append_element("message", str(message))
        self._append_separator()
        return self

    def arguments(self, *args) -> "EventCreator":
        """
        Appends the arguments to the event log.

        :param args: The arguments to append.
        :return: The EventCreator instance.
        """
        self._append_arguments(*args)
        self._append_separator()
        return self

    def thread_id(self) -> "EventCreator":
        """
        Appends the thread ID to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("thread_id", str(threading.get_ident()))
        self._append_separator()
        return self

    def thread_name(self) -> "EventCreator":
        """
        Appends the thread name to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("thread_name", str(threading.current_thread().name))
        self._append_separator()
        return self

    def hostname(self) -> "EventCreator":
        """
        Appends the hostname to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("hostname", str(socket.gethostname()))
        self._append_separator()
        return self

    def ip_address(self) -> "EventCreator":
        """
        Appends the IP address to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("ip_address", str(socket.gethostbyname(socket.gethostname())))
        self._append_separator()
        return self

    def create(self) -> str:
        """
        Creates the event log.

        :return: The event log.
        """
        if self.__event_format == "json":
            self.__event = self.__event.rstrip(self.__format_separator)
            return self.__event + "}"
        elif self.__event_format == "xml":
            self.__event += "</event>"
            return self.__event
        elif self.__event_format == "csv":
            self.__event = self.__event.rstrip(self.__format_separator)
            return self.__event
        else:
            self.__event = self.__event.rstrip(self.__format_separator)
            return self.__event