from pydantic import BaseModel, Field, PrivateAttr

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

    __event: ConfigEvent = PrivateAttr(default_factory=ConfigEvent)
    __log_file: ConfigLogFile = PrivateAttr(default_factory=ConfigLogFile)
    __log_rotate_config: ConfigLogRotate = PrivateAttr(default_factory=ConfigLogRotate)
    __internal_events: ConfigInternalEvents = PrivateAttr(default_factory=ConfigInternalEvents)
    __processors = PrivateAttr(default_factory=default_processors)
    __outputs = PrivateAttr(default_factory=default_outputs)

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