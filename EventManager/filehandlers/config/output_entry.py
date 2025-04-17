
class OutputEntry():
    """
    The `OutputEntry` class represents an output entry in the configuration.
    """
    __name: str
    __parameters: dict[str, object]

    def __init__(self, name: str = "", parameters: dict[str, object] = None):
        self.__name = name
        self.__parameters = parameters if parameters else {}


    @property
    def get_name(self) -> str:
        return self.__name

    @property
    def get_parameters(self) -> dict[str, object]:
        return self.__parameters

    @get_name.setter
    def set_name(self, name: str):
        self.__name = name

    @get_parameters.setter
    def set_parameters(self, parameters: dict[str, object]):
        self.__parameters = parameters