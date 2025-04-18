from EventManager.internal.managerbase import ManagerBase


class InternalEventManager(ManagerBase):
    __prefix: str = "INTERNAL:"

    def __init__(self, log_handler):
        super().__init__(log_handler)
        self._initiate_threads()
        self.log_info("InternalEventManager started successfully.")

    def stop_pipeline(self):
        """
        Stops the event processing pipeline.
        """
        self._stop_all_threads()

    def log_fatal(self, message: str):
        """
        Logs a fatal message.
        :param message: The message to log.
        """
        if self._log_handler.config.internal_events.enabled:
            self.log_message(self.__prefix + "FATAL", message)

    def log_error(self, message: str):
        """
        Logs an error message.
        :param message: The message to log.
        """
        if self._log_handler.config.internal_events.enabled:
            self.log_message(self.__prefix + "ERROR", message)

    def log_warning(self, message: str):
        """
        Logs a warning message.
        :param message: The message to log.
        """
        if self._log_handler.config.internal_events.enabled:
            self.log_message(self.__prefix + "WARNING", message)

    def log_info(self, message: str):
        """
        Logs an info message.
        :param message: The message to log.
        """
        if self._log_handler.config.internal_events.enabled and self._are_info_logs_enabled():
            self.log_message(self.__prefix + "INFO", message)

    def log_debug(self, message: str):
        """
        Logs a debug message.
        :param message: The message to log.
        """
        if self._log_handler.config.internal_events.enabled and self._are_info_logs_enabled():
            self.log_message(self.__prefix + "DEBUG", message)
