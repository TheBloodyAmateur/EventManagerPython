import traceback


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

    def _append_separator(self):
        """
        Appends a separator to the event log.
        """
        if self.__format_separator and self.__event_format not in ["json", "xml"]:
            self.event.append(self.__format_separator)