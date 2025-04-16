
class DefaultProcessors():
    """
    This class contains the default processors that are used in the application.
    """
    @staticmethod
    def createDefault() -> list:
        entry: ProcessorEntry = ProcessorEntry()
        entry.setName("MaskPasswords")
        entry.setParameters(None)
        return list(entry)