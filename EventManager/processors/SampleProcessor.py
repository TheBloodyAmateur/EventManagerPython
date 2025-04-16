from threading import Lock

from EventManager.processors.Processor import Processor


class SampleProcessor(Processor):
    """
    The SampleProcessor class implements the Processor interface and provides functionality to sample events.
    It drops the first N-1 events and keeps every N-th event, where N is the sample size.
    """

    def __init__(self, sample_size: int):
        self._sample_size = sample_size - 1
        self._sample_count = 0
        self._lock = Lock()

    def process_kv(self, event: str) -> str:
        return self._process_event(event)

    def process_json(self, event: str) -> str:
        return self._process_event(event)

    def process_xml(self, event: str) -> str:
        return self._process_event(event)

    def _process_event(self, event: str) -> str:
        with self._lock:
            if self._sample_count < self._sample_size:
                self._sample_count += 1
                return ""  # Drop the event
            else:
                self._sample_count = 0
                return event  # Keep the event
