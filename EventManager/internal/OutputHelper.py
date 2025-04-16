import importlib

from EventManager.outputs.LogOutput import LogOutput
from EventManager.outputs.Output import Output
from EventManager.outputs.PrintOutput import PrintOutput
from EventManager.outputs.SocketOutput import SocketOutput


class OutputHelper():
    """
    A helper class to manage output instances for the EventManager.
    """

    _outputs: list
    __logHandler: LogHandler

    def __init__(self, logHandler: LogHandler):
        """
        Initializes the OutputHelper with a LogHandler.

        :param logHandler: An instance of LogHandler to handle logging.
        """
        self.__logHandler = logHandler

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
