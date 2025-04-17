from EventManager.filehandlers.config.processor_entry import ProcessorEntry


class DefaultProcessors():
    def __init__(self) -> list:
        entry: ProcessorEntry = ProcessorEntry()
        entry.setName("MaskPasswords")
        entry.setParameters(None)
        return list(entry)
