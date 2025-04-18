import inspect
from datetime import datetime

class EventMetaDataBuilder:
    """
    Utility class responsible for constructing event metadata.

    Event metadata typically contains contextual information such as:
    - Timestamp indicating when the event occurred.
    - The log level associated with the event.
    - Class name where the log method was invoked.
    - Method name from which the event was logged.
    - The exact line number within the source file.
    """

    @staticmethod
    def build_metadata(level, log_handler):
        """
        Constructs a metadata dictionary containing contextual information about a logged event.

        :param level: The severity or informational level of the logged event (e.g., INFO, ERROR, DEBUG).
        :param log_handler: The LogHandler instance providing configuration, such as timestamp formatting details.
        :return: A dictionary containing event metadata with keys: "time", "level", "className", "methodName", and "lineNumber".
        """
        # Get the caller's stack frame
        frame = inspect.stack()[3]
        module = inspect.getmodule(frame[0])

        # Format the current timestamp
        time = datetime.now().strftime(log_handler.config.event.time_format)

        # Build metadata dictionary
        metadata = {
            "time": time,
            "level": level,
            "className": module.__name__ if module else "Unknown",
            "methodName": frame.function,
            "lineNumber": str(frame.lineno)
        }
        return metadata