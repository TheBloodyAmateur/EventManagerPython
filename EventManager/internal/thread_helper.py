import queue
import threading


class ThreadHelper():
    __eventThread: threading.Thread
    __processingThread: threading.Thread

    @property
    def get_event_thread(self):
        """
        Returns the event thread.
        :return:
        """
        return self.__eventThread

    @property
    def get_processing_thread(self):
        """
        Returns the processing thread.
        :return:
        """
        return self.__processingThread

    def start_event_thread(self, runnable: callable):
        """
        Starts the event thread with the given runnable function.
        :param runnable:
        :return:
        """
        self.__eventThread = threading.Thread(target=runnable)
        self.__eventThread.start()

    def start_processing_thread(self, runnable: callable):
        """
        Starts the event thread with the given runnable function.
        :param runnable:
        :return:
        """
        self.__eventThread = threading.Thread(target=runnable)
        self.__eventThread.start()

    def stop_thread(self, thread: threading.Thread, q: queue.Queue, remaining_item_processor: callable):
        """
        Stops the thread and processes remaining items in the queue.
        :param thread:
        :param q:
        :param remaining_item_processor:
        :return:
        """
        thread.join(timeout=1)

        # Drain remaining items from the queue
        while not q.empty():
            try:
                event = q.get_nowait()
                if event is not None:
                    remaining_item_processor(event)
            except queue.Empty:
                break
