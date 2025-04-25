Processors
==========

Introduction
------------

Processors are operations which transform or enrich events. When events are logged, they are first passed into the processing queue which applies the processors on the events before forwarding them into the event queue that writes the events to the log file. The default processor is the **MaskPassword** processor, which masks passwords (in case they were logged either willingly or unwillingly).

List of Processors
------------------

There are different types of processors implemented:

* **MaskPasswords**: Masks passwords.
* **EnrichingProcessor**: Enriches events with additional metadata (e.g., IP address of the current machine, hostname, thread name and thread ID, username, Java version, and more).
* **FilterProcessor**: Filters out events that contain one or more specified terms.
* **RegexProcessor**: Matches and replaces terms using regular expressions.
* **SampleProcessor**: Only passes the n-th event to the next stage in the pipeline.

Usage
-----

To add a new Processor to the pipeline, the ``ProcessorEntry`` class can be utilised. In this example, we add a ``RegexProcessor`` which replaces events that have the ``ERROR`` level with the string ``KETCHUP``:

.. code-block:: python

    event_manager = EventManager(log_handler)
    processor_entry = ProcessorEntry(name="RegexProcessor", parameters={
        "regexEntries": [RegexEntry("level", "ERROR", "KETCHUP")]
    })
    event_manager.add_processor(processor_entry)

Processors can also be added to the ``LogHandler``, before the ``EventManager`` instance is initialised:

.. code-block:: python

    processor_entry = ProcessorEntry(name="SampleProcessor", parameters={"sampleSize": 2})
    log_handler.config.processors.append(processor_entry)

Remove and Add Processors
-------------------------

The ``EventManager`` offers methods for both removing and adding processors to the pipeline.

Adding Processors
~~~~~~~~~~~~~~~~~

.. code-block:: python

    processor_entry = ProcessorEntry(name="RegexProcessor", parameters={
        "regexEntries": [RegexEntry("level", "ERROR", "KETCHUP")]
    })

    eventManager.addProcessor(processorEntry);

Removing Processors
~~~~~~~~~~~~~~~~~~~

Processors can be removed using two methods:

1. By specifying the processor name:

   .. code-block:: python

       event_manager.remove_processor("RegexProcessor");

2. By passing the instance of the processor that was originally added:

   .. code-block:: python

       event_manager.remove_processor(processorEntry);
