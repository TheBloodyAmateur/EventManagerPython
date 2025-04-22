"""
EventManager is a logging module designed to be used in a multi-threaded environment.
"""
import time

from EventManager.formatters.event_creator import EventCreator
from EventManager.formatters.key_value_wrapper import KeyValueWrapper
from EventManager.internal.managerbase import ManagerBase
from EventManager.internal_event_manager import InternalEventManager
from EventManager.filehandlers.log_handler import LogHandler


class EventManager(ManagerBase):
    """
    EventManager is a logging module designed to be used in a multithreaded environment.
    It allows for the registration of events and the ability to trigger those events with
    associated data.
    """

    __internal_event_manager: InternalEventManager
    """
    An instance of InternalEventManager that handles the internal event management.
    """

    def __init__(self, log_handler: 'LogHandler' = None, config_path: str = None):
        """
        Initializes the EventManager with either a LogHandler or a configuration file path.

        :param log_handler: An instance of LogHandler.
        :param config_path: Path to the configuration file.
        """
        if log_handler is not None:
            super().__init__(log_handler=log_handler)
        elif config_path is not None:
            super().__init__(config_path=config_path)

        self.__internal_event_manager = self._log_handler.internal_event_manager
        self.__internal_event_manager.log_info("EventManager started successfully.")
        self.__internal_event_manager.log_info("Initializing event thread...")
        self._initiate_threads(self.__internal_event_manager)

    def stop_pipeline(self):
        """
        Stops the event processing pipeline.
        """
        self._stop_all_threads(self.__internal_event_manager)
        self.__internal_event_manager.log_info("EventManager stopped successfully.")
        self.__internal_event_manager.log_info(
            "EventManager stopped successfully. Shutting down internal event manager...")
        self.__internal_event_manager.stop_pipeline()

    @staticmethod
    def set_correct_os_seperator(path: str) -> str:
        """
        Replaces the path separator in the given path with the correct OS-specific separator.

        :param path: The path to be modified.
        :return: The modified path with the correct OS-specific separator.
        """
        import os
        return os.path.normpath(path)

    def log_custom_message(self, log_level: str, message: object):
        """
        Logs a custom message at the specified log level.

        :param log_level: The log level (e.g., INFO, ERROR, DEBUG).
        :param message: The message to be logged.
        """
        self.log_message(log_level, message)

    def log_fatal_message(self, *args):
        """
        Logs a fatal message. Supports:
        - An exception object (extracts stack trace)
        - An EventCreator (calls .create())
        - A single message or string
        - KeyValueWrapper pairs
        """
        if not args:
            return

        first = args[0]

        # Exception with stack trace
        if isinstance(first, Exception):
            stack_trace = self._cast_exception_stack_trace_to_string(first)
            self.log_message("FATAL", stack_trace)

        # EventCreator
        elif isinstance(first, EventCreator):
            self.write_event_to_queue(first.create())

        # KeyValueWrapper-style (assuming multiple structured args)
        elif len(args) > 1 or isinstance(first, KeyValueWrapper):
            self.log_message("FATAL", *args)

        # Simple message (str or other object)
        else:
            self.log_message("FATAL", first)

    def log_error_message(self, *args):
        """
        Logs an error message. Supports:
        - An exception object (extracts stack trace)
        - An EventCreator (calls .create())
        - A single message or string
        - KeyValueWrapper pairs
        """
        if not args:
            return

        first = args[0]

        # Exception with stack trace
        if isinstance(first, Exception):
            stack_trace = self._cast_exception_stack_trace_to_string(first)
            self.log_message("ERROR", stack_trace)

        # EventCreator
        elif isinstance(first, EventCreator):
            self.write_event_to_queue(first.create())

        # KeyValueWrapper-style (assuming multiple structured args)
        elif len(args) > 1 or isinstance(first, KeyValueWrapper):
            self.log_message("ERROR", *args)

        # Simple message (str or other object)
        else:
            self.log_message("ERROR", first)

    def log_warning_message(self, *args):
        """
        Logs a warning message. Supports:
        - An exception object (extracts stack trace)
        - An EventCreator (calls .create())
        - A single message or string
        - KeyValueWrapper pairs
        """
        if not args:
            return

        first = args[0]

        # Exception with stack trace
        if isinstance(first, Exception):
            stack_trace = self._cast_exception_stack_trace_to_string(first)
            self.log_message("WARNING", stack_trace)

        # EventCreator
        elif isinstance(first, EventCreator):
            self.write_event_to_queue(first.create())

        # KeyValueWrapper-style (assuming multiple structured args)
        elif len(args) > 1 or isinstance(first, KeyValueWrapper):
            self.log_message("WARNING", *args)

        # Simple message (str or other object)
        else:
            self.log_message("WARNING", first)

    def log_info_message(self, *args):
        """
        Logs an info message. Supports:
        - An exception object (extracts stack trace)
        - An EventCreator (calls .create())
        - A single message or string
        - KeyValueWrapper pairs
        """
        if not args:
            return
        elif self._are_info_logs_enabled() is False:
            return

        first = args[0]

        # Exception with stack trace
        if isinstance(first, Exception):
            stack_trace = self._cast_exception_stack_trace_to_string(first)
            self.log_message("INFO", stack_trace)

        # EventCreator
        elif isinstance(first, EventCreator):
            self.write_event_to_queue(first.create())

        # KeyValueWrapper-style (assuming multiple structured args)
        elif len(args) > 1 or isinstance(first, KeyValueWrapper):
            self.log_message("INFO", *args)

        # Simple message (str or other object)
        else:
            self.log_message("INFO", first)

    def log_debug_message(self, *args):
        """
        Logs a debug message. Supports:
        - An exception object (extracts stack trace)
        - An EventCreator (calls .create())
        - A single message or string
        - KeyValueWrapper pairs
        """
        if not args:
            return
        elif self._are_info_logs_enabled() is False:
            return

        first = args[0]

        # Exception with stack trace
        if isinstance(first, Exception):
            stack_trace = self._cast_exception_stack_trace_to_string(first)
            self.log_message("DEBUG", stack_trace)

        # EventCreator
        elif isinstance(first, EventCreator):
            self.write_event_to_queue(first.create())

        # KeyValueWrapper-style (assuming multiple structured args)
        elif len(args) > 1 or isinstance(first, KeyValueWrapper):
            self.log_message("DEBUG", *args)

        # Simple message (str or other object)
        else:
            self.log_message("DEBUG", first)

    def monitor(self, operation_name: str, threshold_ms: int, task: callable):
        """
        Monitors the execution time of a task and logs an error message if it exceeds the
        specified threshold.

        :param operation_name: Name of the operation being monitored.
        :param threshold_ms: Duration threshold in nanoseconds.
        :param task: A callable representing the task to run.
        """
        start = time.perf_counter_ns()
        try:
            task()
        except Exception as e:
            stack_trace = self._cast_exception_stack_trace_to_string(e)
            self.log_error_message(stack_trace)
        finally:
            elapsed_ns = time.perf_counter_ns() - start
            elapsed_ms = elapsed_ns / 1_000_000
            if elapsed_ms > threshold_ms:
                message = f"Operation {operation_name} took {int(elapsed_ms)} ms"
                self.log_error_message(message)
