from EventManager.processors.Processor import Processor


class FilterProcessor(Processor):
    """
    The FilterProcessor class implements the Processor interface and provides functionality to filter events.
    """

    __termToFilter: list

    def __init__(self, term_to_filter: list):
        """
        Initializes the FilterProcessor with a list of terms to filter out.

        :param term_to_filter: A list of terms to filter out from the events.
        """
        self.__termToFilter = term_to_filter

    def process_kv(self, event: str) -> str:
        return self.__get_event(event)

    def process_json(self, event: str) -> str:
        return self.__get_event(event)

    def process_xml(self, event: str) -> str:
        return self.__get_event(event)

    def __get_event(self, event: str) -> str:
        for term in self.__termToFilter:
            print(f"term to filter: {term}, event: {event}, event contains term: {term in event}")
            if term not in event:
                return event
        return ""