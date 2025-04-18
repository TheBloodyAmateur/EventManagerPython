class Batch:
    def __init__(self, max_size:int = 65536):
        self.max_size = max_size
        self.events = []
        self.current_size = 0

    def try_add(self, event:str):
        event_size = len(event.encode('utf-8'))
        if self.current_size + event_size > self.max_size:
            return False
        self.events.append(event)
        self.current_size += event_size
        return True

    def get_batch(self):
        return self.events

    def clear_batch(self):
        self.events = []
        self.current_size = 0

    def get_current_size_in_bytes(self):
        return self.current_size
