from pydantic import BaseModel, Field

from EventManager.filehandlers.config.config_event import ConfigEvent
from EventManager.filehandlers.config.config_internal_events import ConfigInternalEvents
from EventManager.filehandlers.config.config_log_file import ConfigLogFile
from EventManager.filehandlers.config.config_log_rotate import ConfigLogRotate
from EventManager.filehandlers.config.helper import default_processors, default_outputs
from EventManager.filehandlers.config.output_entry import OutputEntry
from EventManager.filehandlers.config.processor_entry import ProcessorEntry


class Config(BaseModel):
    """
    The `Config` class manages the configuration settings for the EventManager application.

    It organizes the configuration into the following categories:
    - **ConfigEvent**: Settings related to events.
    - **ConfigLogFile**: Settings related to log files.
    - **ConfigLogRotate**: Settings for log file rotation.
    - **ConfigInternalEvents**: Settings for internal events.
    - **ProcessorEntry**: Settings for event processors.
    """

    __event: ConfigEvent = ConfigEvent()
    __log_file: ConfigLogFile = ConfigLogFile()
    __log_rotate_config: ConfigLogRotate = ConfigLogRotate()
    __internal_events: ConfigInternalEvents = ConfigInternalEvents()
    __processors = default_processors()
    __outputs = default_outputs()

    @property
    def event(self) -> ConfigEvent:
        return self.__event

    @property
    def log_file(self) -> ConfigLogFile:
        return self.__log_file

    @property
    def log_rotate_config(self) -> ConfigLogRotate:
        return self.__log_rotate_config

    @property
    def internal_events(self) -> ConfigInternalEvents:
        return self.__internal_events

    @property
    def processors(self) -> list[ProcessorEntry]:
        return self.__processors

    @property
    def outputs(self) -> list[OutputEntry]:
        return self.__outputs

    def get_processors(self) -> list[ProcessorEntry]:
        """
        Get the list of processors.
        :return: List of processors.
        """
        return self.__processors

    def get_outputs(self) -> list[OutputEntry]:
        """
        Get the list of outputs.
        :return: List of outputs.
        """
        return self.__outputs