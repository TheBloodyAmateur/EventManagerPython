from EventManager.filehandlers.config.output_entry import OutputEntry


class DefaultOutput():
    @staticmethod
    def create_default() -> list:
        entry = OutputEntry()
        entry.set_name("LogOutput")
        entry.set_parameters(None)
        return list(entry)