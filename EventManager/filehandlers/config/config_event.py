from pydantic import BaseModel


class ConfigEvent(BaseModel):
    __debugging_mode: bool = False
    __informational_mode: bool = False
    __time_format: str = "%Y-%m-%d %H:%M:%S"
    __event_format: str = "default"

    @property
    def debugging_mode(self) -> bool:
        return self.__debugging_mode

    @property
    def informational_mode(self) -> bool:
        return self.__informational_mode

    @property
    def time_format(self) -> str:
        return self.__time_format

    @property
    def event_format(self) -> str:
        return self.__event_format

    @debugging_mode.setter
    def debugging_mode(self, debugging_mode: bool):
        self.__debugging_mode = debugging_mode

    @informational_mode.setter
    def informational_mode(self, informational_mode: bool):
        self.__informational_mode = informational_mode

    @time_format.setter
    def time_format(self, time_format: str):
        self.__time_format = time_format

    @event_format.setter
    def event_format(self, event_format: str):
        self.__event_format = event_format