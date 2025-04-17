from pydantic import BaseModel, Field, PrivateAttr

from EventManager.filehandlers.config.config_event import ConfigEvent
from EventManager.filehandlers.config.config_internal_events import ConfigInternalEvents
from EventManager.filehandlers.config.config_log_file import ConfigLogFile
from EventManager.filehandlers.config.config_log_rotate import ConfigLogRotate
from EventManager.filehandlers.config.processor_entry import ProcessorEntry
from EventManager.processors.DefaultProcessors import DefaultProcessors


class Config(BaseModel):
    __event: ConfigEvent = ConfigEvent()
    __log_file: ConfigLogFile = ConfigLogFile()
    __log_rotate_config: ConfigLogRotate = ConfigLogRotate()
    __internal_events: ConfigInternalEvents = ConfigInternalEvents()
    __processors: list[ProcessorEntry] = DefaultProcessors()
    @property
    def get_event(self) -> ConfigEvent:
        return self.__event

    @property
    def get_log_file(self) -> ConfigLogFile:
        return self.__log_file

    @property
    def get_log_rotate_confi(self) -> ConfigLogRotate:
        return self.__log_rotate_config

    @property
    def get_internal_events(self) -> ConfigInternalEvents:
        return self.__internal_events

    @property
    def get_processors(self) -> list[ProcessorEntry]:
        return self.__processors