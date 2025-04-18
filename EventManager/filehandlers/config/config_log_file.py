from pydantic import BaseModel


class ConfigLogFile(BaseModel):
    __file_path: str = "/tmp/"
    __file_name: str = "application"
    __file_extension: str = ".log"

    @property
    def file_path(self) -> str:
        return self.__file_path

    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def file_extension(self) -> str:
        return self.__file_extension

    @file_path.setter
    def file_path(self, file_path: str):
        self.__file_path = file_path

    @file_name.setter
    def file_name(self, file_name: str):
        self.__file_name = file_name

    @file_extension.setter
    def file_extension(self, file_extension: str):
        self.__file_extension = file_extension