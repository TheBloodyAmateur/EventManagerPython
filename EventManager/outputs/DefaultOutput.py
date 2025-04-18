from EventManager.filehandlers.config.output_entry import OutputEntry


class DefaultOutput():
    """
    A default output class that provides a static method to create a default output entry.
    """
    @staticmethod
    def create_default() -> list:
        entry = OutputEntry()
        entry.name("LogOutput")
        entry.parameters(None)
        return list(entry)
