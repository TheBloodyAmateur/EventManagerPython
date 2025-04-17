from pydantic import BaseModel


class ConfigLogFile(BaseModel):
    __file_path: str = "/tmp/"
    __file_name: str = "application"
    __file_extension: str = ".log"

    @property
    def get_file_path(self) -> str:
        return self.__file_path

    @property
    def get_file_name(self) -> str:
        return self.__file_name

    @property
    def get_file_extension(self) -> str:
        return self.__file_extension

    @get_file_path.setter
    def set_file_path(self, file_path: str):
        self.__file_path = file_path

    @get_file_name.setter
    def set_file_name(self, file_name: str):
        self.__file_name = file_name

    @get_file_extension.setter
    def set_file_extension(self, file_extension: str):
        self.__file_extension = file_extension