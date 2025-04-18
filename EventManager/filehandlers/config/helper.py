import atomics

from EventManager.filehandlers.config.output_entry import OutputEntry
from EventManager.filehandlers.config.processor_entry import ProcessorEntry


def atomic_int(initial: int) -> atomics.atomic:
    """
    Create an atomic integer with a specified initial value.
    :param initial: The initial value for the atomic integer.
    :return: An atomic integer initialized to the specified value.
    """
    a = atomics.atomic(width=4, atype=atomics.INT)
    a.store(initial)
    return a


def default_processors() -> list[ProcessorEntry]:
    """
    Create a list of default processors for the EventManager.
    :return:  A list containing a single ProcessorEntry instance.
    """
    entry: ProcessorEntry = ProcessorEntry()
    entry.name = "MaskPasswords"
    entry.parameters = None
    return [entry]

def default_outputs() -> list[OutputEntry]:
    """
    Create a list of default outputs for the EventManager.
    :return:  A list containing a single OutputEntry instance.
    """
    entry: OutputEntry = OutputEntry()
    entry.name = "LogOutput"
    entry.parameters = None
    return [entry]