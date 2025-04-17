from pydantic import BaseModel


class ConfigEvent(BaseModel):
    __debugging_mode: bool = False
    __informational_mode: bool = False
    __time_format: str = "%Y-%m-%d %H:%M:%S"
    __event_format: str = "default"

    @property
    def get_debugging_mode(self) -> bool:
        return self.__debugging_mode

    @property
    def get_informational_mode(self) -> bool:
        return self.__informational_mode

    @property
    def get_time_format(self) -> str:
        return self.__time_format

    @property
    def get_event_format(self) -> str:
        return self.__event_format

    @get_debugging_mode.setter
    def set_debugging_mode(self, debugging_mode: bool):
        self.__debugging_mode = debugging_mode

    @get_informational_mode.setter
    def set_informational_mode(self, informational_mode: bool):
        self.__informational_mode = informational_mode

    @get_time_format.setter
    def set_time_format(self, time_format: str):
        self.__time_format = time_format

    @get_event_format.setter
    def set_event_format(self, event_format: str):
        self.__event_format = event_format