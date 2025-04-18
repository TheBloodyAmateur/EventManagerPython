import importlib

from EventManager.outputs.LogOutput import LogOutput
from EventManager.outputs.PrintOutput import PrintOutput
from EventManager.outputs.SocketOutput import SocketOutput
from EventManager.filehandlers.log_handler import LogHandler
from EventManager.outputs.Output import Output
from EventManager.filehandlers.config.output_entry import OutputEntry

class OutputHelper():
    """
    A helper class to manage output instances for the EventManager.
    """

    _outputs: list
    __log_handler: LogHandler

    def __init__(self, log_handler: LogHandler):
        """
        Initializes the OutputHelper with a LogHandler.

        :param log_handler: An instance of LogHandler to handle logging.
        """
        self.__log_handler = log_handler

    def __create_output_instance(self, class_name: str, parameters: dict = None) -> Output:
        try:
            package_prefix = "EventManager.outputs"
            module = importlib.import_module(f"{package_prefix}.{class_name.lower()}")
            clazz = getattr(module, class_name)

            output_instance = self.get_output(parameters, clazz)
            if output_instance is not None:
                return output_instance

            return clazz()  # fallback to default constructor
        except Exception as e:
            return None

    def get_output(self, parameters: dict, clazz) -> Output:
        if parameters is None:
            return None

        if clazz.__name__ == "PrintOutput":
            return PrintOutput()
        elif clazz.__name__ == "LogOutput":
            return LogOutput()
        elif clazz.__name__ == "SocketOutput":
            socket_settings = parameters.get("socketSettings", [])
            return SocketOutput(socket_settings)

        return None

    def initialise_outputs(self) -> list:
        """
        Initializes the outputs based on the configuration provided in the LogHandler.
        :return: A list of initialized output instances.
        """
        outputs = []
        for entry in self.__log_handler.config.get_outputs():
            output_instance = self.__create_output_instance(entry.name(), entry.parameters())
            if output_instance is not None:
                outputs.append(output_instance)
        return outputs

    def output_event(self, event: str, internal_event_manager=None):
        """
        Outputs the event to all output destinations.

        :param event: The event message to output.
        :param internal_event_manager: Optional custom event manager to use for writing.
                                       Defaults to self._log_handler if not provided.
        """
        context = internal_event_manager or self.__log_handler
        for output in self._outputs:
            output.write(context, event)

    def __is_output_already_registered(self, output, outputs):
        return any(type(p) == type(output) for p in outputs)

    def add_new_output(self, output_entry):
        if output_entry is None:
            return
        output_instance = self.__create_output_instance(output_entry.get_name(), output_entry.get_parameters())
        if output_instance is not None and not self.__is_output_already_registered(output_instance):
            self._outputs.append(output_instance)

    def add_output(self, output_entry):
        if output_entry is None:
            return False
        self.add_new_output(output_entry)
        return True

    def remove_output(self, output):
        """
        Removes an output destination.

        :param output: Either the class name as a string or an OutputEntry instance.
        :return: True if the output was removed, False otherwise.
        """
        if output is None:
            return False

        if isinstance(output, str):
            for existing_output in self._outputs:
                if existing_output.__class__.__name__.lower() == output.lower():
                    self._outputs.remove(existing_output)
                    return True

        elif isinstance(output, OutputEntry):
            instance = self.__create_output_instance(output.get_name, output.get_parameters)
            for existing_output in self._outputs:
                if type(existing_output) is type(instance):
                    self._outputs.remove(existing_output)
                    return True

        return False
