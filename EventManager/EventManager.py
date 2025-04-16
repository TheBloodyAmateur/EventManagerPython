from EventManager.internal.ManagerBase import ManagerBase


class EventManager(ManagerBase):
    """
    EventManager is a logging module designed to be used in a multi-threaded environment.
    It allows for the registration of events and the ability to trigger those events with
    associated data.
    """

    __internalEventManager: InternalEventManager
    """
    An instance of InternalEventManager that handles the internal event management.
    """

    def __init__(self, logHandler: LogHandler):
        """
        Initializes the EventManager with a LogHandler.

        :param logHandler: An instance of LogHandler to handle logging.
        """
        super().__init__(logHandler)
        self.__internalEventManager = logHandler.getInternalEventManager()
        self.__internalEventManager.logInfo("EventManager started successfully.")
        self.__internalEventManager.logInfo("Initializing event thread...");
        initiateThreads(self.__internalEventManager)

    def __init__(self, configPath: str):
        """
        Initializes the EventManager with a configuration file.

        :param configPath: Path to the configuration file.
        """
        super().__init__(configPath)
        self.__internalEventManager = logHandler.getInternalEventManager()
        __internalEventManager.logInfo("EventManager started successfully.")
        __internalEventManager.logInfo("Initializing event thread...");
        initiateThreads(internalEventManager)
