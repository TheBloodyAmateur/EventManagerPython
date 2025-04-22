import importlib
from typing import Union

from EventManager.filehandlers.config.processor_entry import ProcessorEntry
from EventManager.processors import Processor
from EventManager.processors.enrichingprocessor import EnrichingProcessor
from EventManager.processors.filterprocessor import FilterProcessor
from EventManager.processors.maskipv4address import MaskIPV4Address
from EventManager.processors.maskpasswords import MaskPasswords
from EventManager.processors.regexprocessor import RegexProcessor
from EventManager.processors.sampleprocessor import SampleProcessor


class ProcessorHelper():
    """
    The ProcessorHelper class is responsible for managing and processing events
    """
    __log_handler = None

    def __init__(self, log_handler):
        """
        Initializes the ProcessorHelper with a LogHandler.

        :param log_handler: An instance of LogHandler to handle logging.
        """
        self.__log_handler = log_handler
        self._processors = []

    def __create_processor_instance(self, class_name: str, parameters: dict = None) -> Processor:
        """
        Creates an instance of a processor class based on the provided class name and parameters.

        :param class_name: The name of the processor class to instantiate.
        :param parameters: A dictionary of parameters to pass to the processor constructor.
        :return: An instance of the specified processor class.
        """
        try:
            package_prefix = "EventManager.processors"
            module = importlib.import_module(f"{package_prefix}.{class_name.lower()}")
            clazz = getattr(module, class_name)

            exclude_ranges = self.__get_processor(parameters, clazz)
            if exclude_ranges is not None:
                return exclude_ranges

            return clazz()  # Instantiate the class
        except Exception as e:
            print(f"Error creating processor instance: {e}")
            return None

    def __get_processor(self, parameters: dict, clazz) -> Processor:
        """
        Retrieves a processor instance based on the provided parameters and class.

        :param parameters: A dictionary of parameters to pass to the processor constructor.
        :param clazz: The class of the processor to instantiate.
        :return: An instance of the specified processor class.
        """
        try:
            if clazz == MaskIPV4Address:
                exclude_ranges = parameters.get("excludeRanges", [])
                return MaskIPV4Address(exclude_ranges)
            elif clazz == EnrichingProcessor:
                enriching_fields = parameters.get("enrichingFields", [])
                return EnrichingProcessor(enriching_fields)
            elif clazz == RegexProcessor:
                regex_entries = parameters.get("regexEntries", [])
                return RegexProcessor(regex_entries)
            elif clazz == FilterProcessor:
                term_to_filter = parameters.get("termToFilter", [])
                return FilterProcessor(term_to_filter)
            elif clazz == SampleProcessor:
                sample_size = parameters.get("sampleSize", 0)
                return SampleProcessor(sample_size)
            elif clazz == MaskPasswords:
                return MaskPasswords()
        except (TypeError, KeyError):
            return None
        return None

    def __is_processor_already_registered(self, processor):
        """
        Checks if a Processor is already registered.

        :param processor: The processor to check.
        :return: True if the processor is already registered, False otherwise.
        """
        return any(p.__class__ == processor.__class__ for p in self._processors)

    def process_event(self, event: str):
        """
        Processes an event by passing it through all registered processors.

        :param event: The event to process.
        :return: The processed event.
        """
        for processor in self._processors:
            event_format = self.__log_handler.config.event.event_format
            if event_format == "kv":
                event = processor.process_kv(event)
            elif event_format == "xml":
                event = processor.process_xml(event)
            elif event_format == "json":
                event = processor.process_json(event)
        return event

    def initialise_processors(self):
        """
        Initializes the processors by creating instances based on the configuration.
        :return:
        """
        test = self.__log_handler.config.get_processors()
        for entry in test:
            processor = self.__create_processor_instance(entry.name, entry.parameters)
            if processor and not self.__is_processor_already_registered(processor):
                self._processors.append(processor)

    def add_processor(self, processor_entry):
        """
        Adds a processor to the list of registered processors.
        :param processor_entry: The processor entry to add.
        :return: True if the processor was added, False otherwise.
        """
        if not processor_entry:
            return False

        processor = self.__create_processor_instance(processor_entry.name, processor_entry.parameters)
        if processor and not self.__is_processor_already_registered(processor):
            self._processors.append(processor)
            return True
        return False

    def remove_processor_by_name(self, processor_name):
        """
        Removes a processor by its name from the list of registered processors.
        :param processor_name: The name of the processor to remove.
        :return: True if the processor was removed, False otherwise.
        """
        if not processor_name:
            return False
        for processor in self._processors:
            if processor.__class__.__name__.lower() == processor_name.lower():
                self._processors.remove(processor)
                return True
        return False

    def remove_processor(self, identifier: Union[str, 'ProcessorEntry']) -> bool:
        """
        Removes a processor from the list of registered processors based on the provided identifier.
        :param identifier: Either a string representing the processor name or a ProcessorEntry object.
        :return: True if the processor was removed, False otherwise.
        """
        if identifier is None:
            return False

        if isinstance(identifier, str):
            for processor in self._processors:
                if processor.__class__.__name__.lower() == identifier.lower():
                    self._processors.remove(processor)
                    return True

        elif hasattr(identifier, 'getParameters'):
            for processor in self._processors:
                output_instance = self.__get_processor(identifier.getParameters(), processor.__class__)
                if processor.__class__ == output_instance.__class__:
                    self._processors.remove(processor)
                    return True

        return False