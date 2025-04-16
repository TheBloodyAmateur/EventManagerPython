from EventManager.outputs.Output import Output


class PrintOutput(Output):
    """
    A class to handle print output for events.
    """

    def write(self, event: str):
        """
        Writes the event to the standard output.

        :param event: The event to be written.
        """
        print(event)

    def write(self, internal_event_manager: 'InternalEventManager', event: str):
        """
        Writes the event to the standard output.

        :param internal_event_manager: InternalEventManager instance to handle logging.
        :param event: The event to be written.
        """
        print(event)