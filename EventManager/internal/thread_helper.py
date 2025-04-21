import queue
import threading


class ThreadHelper:
    """
    A helper class to manage threads in the EventManager.
    """

    def __init__(self):
        """
        Initializes the ThreadHelper.
        """
        self.__event_thread: threading.Thread
        self.__processing_thread: threading.Thread
        self.__event_thread_event: threading.Event = threading.Event()
        self.__processing_thread_event: threading.Event = threading.Event()

    @property
    def event_thread(self):
        """
        Returns the event thread.
        :return:
        """
        return self.__event_thread

    @property
    def processing_thread(self):
        """
        Returns the processing thread.
        :return:
        """
        return self.__processing_thread

    def start_event_thread(self, runnable: callable):
        """
        Starts the event thread with the given runnable function.
        :param runnable:
        :return:
        """
        self.__event_thread_event.clear()
        self.__event_thread = threading.Thread(target=lambda : runnable(self.__event_thread_event))
        self.__event_thread.start()

    def start_processing_thread(self, runnable: callable):
        """
        Starts the event thread with the given runnable function.
        :param runnable:
        :return:
        """
        self.__processing_thread_event.clear()
        self.__processing_thread = threading.Thread(target=lambda : runnable(self.__processing_thread_event))
        self.__processing_thread.start()

    def stop_thread(self, thread_name: str, thread: threading.Thread, q: queue.Queue, remaining_item_processor: callable):
        """
        Stops the thread and processes remaining items in the queue.
        :param thread:
        :param q:
        :param remaining_item_processor:
        :return:
        """

        # Check to which thread the thread_name corresponds
        if thread_name == "event":
            self.__event_thread_event.set()
        elif thread_name == "process":
            self.__processing_thread_event.set()

        thread.join(timeout=1)

        # Drain remaining items from the queue
        while not q.empty():
            try:
                event = q.get_nowait()
                if event is not None:
                    remaining_item_processor(event)
            except queue.Empty:
                break