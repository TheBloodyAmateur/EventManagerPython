from EventManager.internal import ThreadHelper


class ManagerBase():
    _logHandler: LogHandler
    _processorHelper: ProcessorHelper
    _outputHelper: OutputHelper
    # TODO: Add change the java class name for the queue to a pythonic equivalent
    _eventQueue: LinkedBlockingQueue
    _processingQueue: LinkedBlockingQueue
    _threadHelper: ThreadHelper

    def __init__(self, logHandler: LogHandler):
        """
        Initializes the ManagerBase with a LogHandler.

        :param logHandler: An instance of LogHandler to handle logging.
        """
        self._logHandler = logHandler
        self._processorHelper = ProcessorHelper(logHandler)
        self._outputHelper = OutputHelper(logHandler)

    def __init__(self, configPath: str):
        """
        Initializes the ManagerBase with a LogHandler.

        :param logHandler: An instance of LogHandler to handle logging.
        """
        self._logHandler = LogHandler(configPath)
        self._processorHelper = ProcessorHelper(logHandler)
        self._outputHelper = OutputHelper(logHandler)

    def _initiate_threads(self):
        """
        Initializes the threads for processing events and outputting results.
        """
        initialiseProcessorThreadAndOutputs()
