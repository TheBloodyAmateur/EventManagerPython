from pydantic import BaseModel
import atomics

from EventManager.filehandlers.config.helper import atomic_int


class ConfigLogRotate(BaseModel):
    __max_size_in_KB: atomics.atomic = 10240
    __rotation_period_in_seconds: atomics.atomic = 86400
    __compression_format: str = "gzip"

    @property
    def get_max_size_in_KB(self) -> int:
        return self.__max_size_in_KB.load()

    @property
    def get_rotation_period_in_seconds(self) -> int:
        return self.__rotation_period_in_seconds.load()

    @property
    def get_compression_format(self) -> str:
        return self.__compression_format

    @get_max_size_in_KB.setter
    def set_max_size_in_KB(self, value: int):
        self.__max_size_in_KB.store(value)

    @get_rotation_period_in_seconds.setter
    def set_rotation_period_in_seconds(self, value: int):
        self.__rotation_period_in_seconds.store(value)

    @get_compression_format.setter
    def set_compression_format(self, value: str):
        self.__compression_format = value