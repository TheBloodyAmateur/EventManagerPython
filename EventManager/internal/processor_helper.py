from EventManager.filehandlers.log_handler import LogHandler
from EventManager.processors import Processor, MaskIPV4Address, EnrichingProcessor, RegexProcessor, FilterProcessor, \
    SampleProcessor


class ProcessorHelper():
    __processors: list
    __log_handler: LogHandler

    def __init__(self, log_handler: LogHandler):
        """
        Initializes the ProcessorHelper with a LogHandler.

        :param log_handler: An instance of LogHandler to handle logging.
        """
        self.__log_handler = log_handler

    def __create_processor_instance(self, class_name: str, parameters: dict = None) -> Processor:
        """
        Creates an instance of a processor class based on the provided class name and parameters.

        :param class_name: The name of the processor class to instantiate.
        :param parameters: A dictionary of parameters to pass to the processor constructor.
        :return: An instance of the specified processor class.
        """
        try:
            package_prefix = "com.github.eventmanager.processors."
            full_class_name = package_prefix + class_name

            # Dynamically import the module and class
            module_name, class_name = full_class_name.rsplit('.', 1)
            module = __import__(module_name, fromlist=[class_name])
            clazz = getattr(module, class_name)

            exclude_ranges = self.__get_processor(parameters, clazz)
            if exclude_ranges is not None:
                return exclude_ranges

            return clazz()  # Instantiate the class
        except Exception as e:
            return None

    def __get_processor(self, parameters: dict, clazz) -> Processor:
        """
        Retrieves a processor instance based on the provided parameters and class.

        :param parameters: A dictionary of parameters to pass to the processor constructor.
        :param clazz: The class of the processor to instantiate.
        :return: An instance of the specified processor class.
        """
        if parameters is None:
            return None
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
        except (TypeError, KeyError):
            return None
        return None

    def __is_processor_already_registered(self, processor, processors):
        """
        Checks if a Processor is already registered.

        :param processor: The processor to check.
        :param processors: The list of registered processors.
        :return: True if the processor is already registered, False otherwise.
        """
        return any(p.__class__ == processor.__class__ for p in processors)

    def process_event(self, event: str, processors, log_handler:LogHandler):
        """
        Processes an event by passing it through all registered processors.

        :param event: The event to process.
        :param processors: List of registered processors.
        :param log_handler: Log handler containing configuration details.
        :return: The processed event.
        """
        for processor in processors:
            event_format = log_handler.get_config.get_event.get_event_format
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
        for entry in self.__log_handler.get_config.get_processors:
            processor = self.__create_processor_instance(entry.get_name, entry.get_parameters)
            if processor and not self.__is_processor_already_registered(processor):
                self.__processors.append(processor)

    def add_processor(self, processor_entry):
        """
        Adds a processor to the list of registered processors.
        :param processor_entry: The processor entry to add.
        :return: True if the processor was added, False otherwise.
        """
        if not processor_entry:
            return False

        processor = self.__create_processor_instance(processor_entry.get_name(), processor_entry.get_parameters())
        if processor and not self.__is_processor_already_registered(processor):
            self.__processors.append(processor)
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
        for processor in self.__processors:
            if processor.__class__.__name__.lower() == processor_name.lower():
                self.__processors.remove(processor)
                return True
        return False

    def remove_processor(self, processor_entry):
        """
        Removes a processor from the list of registered processors based on its entry.
        :param processor_entry: The processor entry to remove.
        :return: True if the processor was removed, False otherwise.
        """
        if not processor_entry:
            return False
        for processor in self.__processors:
            output_instance = self.__get_processor(processor_entry.get_parameters(), processor.__class__)
            if processor.__class__ == output_instance.__class__:
                self.__processors.remove(processor)
                return True
        return False