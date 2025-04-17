from pydantic import BaseModel


class ConfigInternalEvents(BaseModel):
    __file_path: str = "/tmp/"
    __file_name: str = "internal_events.log"
    __file_extension: str = ".log"
    __enabled: bool = True

    @property
    def get_file_path(self) -> str:
        return self.__file_path

    @property
    def get_file_name(self) -> str:
        return self.__file_name

    @property
    def get_file_extension(self) -> str:
        return self.__file_extension

    @property
    def get_enabled(self) -> bool:
        return self.__enabled

    @get_file_path.setter
    def set_file_path(self, value: str):
        self.__file_path = value

    @get_file_name.setter
    def set_file_name(self, value: str):
        self.__file_name = value

    @get_file_extension.setter
    def set_file_extension(self, value: str):
        self.__file_extension = value

    @get_enabled.setter
    def set_enabled(self, value: bool):
        self.__enabled = value