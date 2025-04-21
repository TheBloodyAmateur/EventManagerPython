from pydantic import BaseModel


class ConfigInternalEvents(BaseModel):
    __file_path: str = "/tmp/"
    __file_name: str = "internal_events"
    __file_extension: str = ".log"
    __enabled: bool = True

    @property
    def file_path(self) -> str:
        return self.__file_path

    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def file_extension(self) -> str:
        return self.__file_extension

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @file_path.setter
    def file_path(self, value: str):
        self.__file_path = value

    @file_name.setter
    def file_name(self, value: str):
        self.__file_name = value

    @file_extension.setter
    def file_extension(self, value: str):
        self.__file_extension = value

    @enabled.setter
    def enabled(self, value: bool):
        self.__enabled = value