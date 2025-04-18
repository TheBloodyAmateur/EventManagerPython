import threading
import traceback

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

    __stack_trace_element: traceback.StackSummary = traceback.extract_stack()
    __class_name: str = __stack_trace_element[-2].name
    __method_name: str = __stack_trace_element[-1].name
    __line_number: int = __stack_trace_element[-1].lineno
    __event: str = ""
    __event_format: str
    __formatter: EventFormatter
    __format_separator: str = " "

    def __init__(self, format="key-value"):
        """
        The constructor of the EventCreator class.

        :param format: The format of the event log. The format can be one of the following: "json", "xml", "csv", or
                       "key-value". If the format is not one of the specified formats, the default format is "key-value".
        """

        if format == "json":
            self.event = {}
            self.format_separator = ","
        elif format == "xml":
            self.event = ["<event>"]
        elif format == "csv":
            self.format_separator = ","
        else:
            self.format_separator = " "

    def _append_element(self, key, value):
        """
        Appends a key-value pair to the event. In case the format is "csv", only the value is appended.

        :param key: The key.
        :param value: The value.
        """
        if self.__event_format == "json":
            self.event[key] = value
        elif self.__event_format == "xml":
            self.event.append(f"<{key}>{value}</{key}>")
        elif self.__event_format == "csv":
            self.event.append(value)
        else:
            self.event.append(f"{key}={value}")

    def _append_arguments(self, *args):
        """
        Appends the arguments to the event log.

        :param args: The arguments to append.
        """
        for arg in args:
            self._append_element("argument", arg)
            self._append_separator()

    def _append_separator(self):
        """
        Appends a separator to the event log.
        """
        if self.__format_separator and self.__event_format not in ["json", "xml"]:
            self.event.append(self.__format_separator)

    def line_number(self) -> "EventCreator":
        """
        Appends the line number to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("line_number", self.__line_number)
        return self

    def class_name(self) -> "EventCreator":
        """
        Appends the class name to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("class_name", self.__class_name)
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
            self._append_element("timestamp", time.strftime(timestamp_format))
        else:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            self._append_element("timestamp", timestamp)
        self._append_separator()
        return self

    def level(self, level: str) -> "EventCreator":
        """
        Appends the level to the event log.

        :param level: The level of the event log.
        :return: The EventCreator instance.
        """
        self._append_element("level", level)
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
        self._append_element("message", message)
        self._append_separator()
        return self

    def arguments(self, *args) -> "EventCreator":
        """
        Appends the arguments to the event log.

        :param args: The arguments to append.
        :return: The EventCreator instance.
        """
        self._append_arguments(*args)
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
        self._append_element("thread_name", threading.current_thread().name)
        self._append_separator()
        return self

    def hostname(self) -> "EventCreator":
        """
        Appends the hostname to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("hostname", threading.get_ident())
        self._append_separator()
        return self

    def ip_address(self) -> "EventCreator":
        """
        Appends the IP address to the event log.

        :return: The EventCreator instance.
        """
        self._append_element("ip_address", threading.get_ident())
        self._append_separator()
        return self

    def create(self) -> str:
        """
        Creates the event log.

        :return: The event log.
        """
        if self.__event_format == "json":
            return str(self.event).replace("'", '"')
        elif self.__event_format == "xml":
            self.event.append("</event>")
            return "".join(self.event)
        elif self.__event_format == "csv":
            return self.format_separator.join(self.event)
        else:
            return self.format_separator.join(self.event)