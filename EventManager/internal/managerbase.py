import queue
import threading
from typing import TYPE_CHECKING

from EventManager.filehandlers.config.output_entry import OutputEntry
from EventManager.filehandlers.config.processor_entry import ProcessorEntry
from EventManager.formatters.event_formatter import EventFormatter
from EventManager.internal.event_metadata_builder import EventMetaDataBuilder
from EventManager.internal.processor_helper import ProcessorHelper
from EventManager.internal.thread_helper import ThreadHelper

if TYPE_CHECKING:
    from EventManager.internal.output_helper import OutputHelper


class ManagerBase:

    def __init__(self, log_handler = None, config_path: str = None):
        """
        Initializes the ManagerBase with either a LogHandler or a config path.

        :param log_handler: An existing LogHandler instance.
        :param config_path: A path to a config file to create a LogHandler.
        """

        from EventManager.filehandlers.log_handler import LogHandler
        from EventManager.internal.output_helper import OutputHelper

        self._processor_helper: 'ProcessorHelper'
        self._output_helper: 'OutputHelper'
        self._event_queue: queue = queue.Queue()
        self._processing_queue: queue = queue.Queue()
        self._thread_helper: 'ThreadHelper' = ThreadHelper()

        if log_handler:
            self._log_handler: 'LogHandler' = log_handler
        elif config_path:
            self._log_handler: 'LogHandler' = LogHandler(config_path)

        self._processor_helper = ProcessorHelper(self._log_handler)
        self._output_helper = OutputHelper(self._log_handler)

    @property
    def log_handler(self):
        """
        Returns the LogHandler instance.
        """
        return self._log_handler

    def _initiate_threads(self, internal_event_manager=None):
        """
        Initializes the threads for processing events and outputting results.

        :param internal_event_manager: Optional InternalEventManager instance.
                                       If not provided, uses self.__log_handler.
        """
        self.__initialise_processor_thread_and_outputs()

        def event_thread(stop_event: threading.Event):
            while not stop_event.is_set():
                try:
                    event = self._event_queue.get(timeout=0.1)
                    if internal_event_manager:
                        self.output_event(event, internal_event_manager)
                    else:
                        self.output_event(event)
                except queue.Empty:
                    continue

        self._thread_helper.start_event_thread(event_thread)

    def __initialise_processor_thread_and_outputs(self):
        """
        Initializes the processing thread and output destinations.
        """
        self._processor_helper.initialise_processors()
        self._output_helper.initialise_outputs(self)

        def processing_thread(stop_event: threading.Event):
            while not stop_event.is_set():
                try:
                    event = self._processing_queue.get(timeout=0.1)
                    event = self._processor_helper.process_event(event)
                    if event and event.strip():
                        self.write_event_to_queue(event)
                except queue.Empty:
                    continue

        self._thread_helper.start_processing_thread(processing_thread)

    def _stop_all_threads(self, internal_event_manager=None):
        """
        Stops all threads gracefully and processes remaining events.
        """
        def process_remaining_event(event):
            try:
                event = self._processor_helper.process_event(event)
                self.write_event_to_queue(event)
            except Exception as e:
                if internal_event_manager:
                    internal_event_manager.log_error(f"Error processing remaining events: {str(e)}")
                else:
                    print(f"Error processing remaining events: {str(e)}")

        self._thread_helper.stop_thread(
            "process", self._thread_helper.processing_thread, self._processing_queue, process_remaining_event
        )

        def output_remaining_event(event):
            try:
                self.output_event(event)
            except Exception as e:
                if internal_event_manager:
                    internal_event_manager.log_error(f"Error writing remaining events: {str(e)}")
                else:
                    print(f"Error writing remaining events: {str(e)}")

        self._thread_helper.stop_thread(
            "event", self._thread_helper.processing_thread, self._event_queue, output_remaining_event
        )

    def write_event_to_queue(self, event):
        """
        Adds processed event to the event queue.
        """
        self._event_queue.put(event)

    def write_event_to_processing_queue(self, event):
        """
        Adds raw event to the processing queue.
        """
        self._processing_queue.put(event)

    def output_event(self, event:str, internal_event_manager=None):
        """
        Passes the event to the output destinations.
        """
        self._output_helper.output_event(event, internal_event_manager)

    def log_message(self, level: str, *messages):
        """
        Formats and queues a log message for processing and eventual writing to log file.

        :param level: Log level (e.g., INFO, ERROR).
        :param messages: A single message (Exception or str), or multiple KeyValueWrapper instances.
        """
        meta_data = EventMetaDataBuilder.build_metadata(level, self._log_handler)
        event_format = self._log_handler.config.event.event_format

        if len(messages) == 1 and isinstance(messages[0], (str, Exception)):
            # Handle single message string or exception
            message = messages[0]
            formatted = message.args[0] if isinstance(message, Exception) else str(message)

            formatter = {
                "kv": EventFormatter.KEY_VALUE,
                "csv": EventFormatter.CSV,
                "xml": EventFormatter.XML,
                "json": EventFormatter.JSON
            }.get(event_format, EventFormatter.DEFAULT)

            event = formatter.format_message(meta_data, formatted)
        else:
            # Handle structured key-value messages
            formatter = {
                "kv": EventFormatter.KEY_VALUE,
                "csv": EventFormatter.CSV,
                "xml": EventFormatter.XML,
                "json": EventFormatter.JSON
            }.get(event_format, EventFormatter.DEFAULT)

            event = formatter.format(meta_data, *messages)

        self.write_event_to_processing_queue(event)

    def add_output(self, output_entry: 'OutputEntry') -> bool:
        """
        Adds a new output destination based on the provided OutputEntry.
        :param output_entry: The OutputEntry instance containing the output configuration.
        :return: True if the output was added successfully, False otherwise.
        """
        return self._output_helper.add_output(output_entry)

    def remove_output(self, output):
        """
        Removes an output destination.

        :param output: Either an OutputEntry object or a class name as a string.
        :return: True if the output was removed successfully, False otherwise.
        """
        if isinstance(output, str):
            return self._output_helper.remove_output(output)
        else:
            return self._output_helper.remove_output(output)

    def add_processor(self, processor):
        """
        Adds a processor to the processing queue.

        :param processor: The processor to be added.
        """
        self._processor_helper.add_processor(processor)

    def remove_processor(self, processor: ProcessorEntry = None, processor_name: str = None):
        """
        Removes a processor from the processing queue.

        :param processor: The processor to be removed.
        :param processor_name: The name of the processor to be removed.
        """
        processor = processor or processor_name
        self._processor_helper.remove_processor(processor)

    def _cast_exception_stack_trace_to_string(self) -> str:
        """
        Converts the stack trace of an exception to a string.
        :return: The stack trace as a string.
        """
        import traceback
        import sys

        exc_type, exc_value, exc_tb = sys.exc_info()
        return "".join(traceback.format_exception(exc_type, exc_value, exc_tb))

    def _are_info_logs_enabled(self) -> bool:
        """
        Checks if information or debugging logs are enabled.
        :return: True if information or debugging logs are enabled, False otherwise.
        """
        information_mode = self._log_handler.config.event.informational_mode
        debugging_mode = self._log_handler.config.event.debugging_mode
        return information_mode or debugging_mode

