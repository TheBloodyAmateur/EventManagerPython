Output Destinations
===================

Introduction
------------

Outputs are destinations to which events are sent. After events have been computed by the Processors, they are passed to a list of Outputs which essentially define where the events are sent.

List of Outputs
---------------

For the time being, there are three Output destinations an event can be sent to:

* **PrintOutput**: Printed out to the console.
* **LogOutput**: Written to a log file.
* **SocketOutput**: Sent to a socket.

Usage
-----

To add a new Output to the pipeline, the ``OutputEntry`` class can be utilised. In this example, we add a socket destination by creating an ``OutputEntry`` instance and setting the properties for the ``SocketOutput``:

.. code-block:: python

    log_handler: LogHandler = LogHandler("config/path/config.json")
    socket_entry: OutputEntry = OutputEntry(name="SocketOutput", parameters={
        "socketSettings": [SocketEntry("localhost", 6000)]
    })
    log_handler.config.outputs.append(socket_entry)

Instances of the ``OutputEntry`` class can also be added after the EventManager was initialised:

.. code-block:: python

    log_handler = LogHandler("config/path/config.json")
    log_handler.config.event.event_format = "json"
    output_entry = OutputEntry(name="PrintOutput")
    log_handler.config.outputs.append(output_entry)

Remove and Add Outputs
----------------------

The ``EventManager`` offers methods for both removing Outputs from the pipeline, and adding them.

Adding Outputs
~~~~~~~~~~~~~~

To add an Output to the pipeline, the ``addOutput`` method can be used:

.. code-block:: python

    log_handler = LogHandler("config/path/config.json")
    log_handler.config.event.event_format = "json"
    output_entry = OutputEntry(name="PrintOutput")
    log_handler.config.outputs.append(output_entry)

Removing Outputs
~~~~~~~~~~~~~~~~

There are two methods to remove Outputs:

1. By the name of the class:

   .. code-block:: python

       event_manager.remove_output("PrintOutput")

2. By passing the instance with which the Output was added:

   .. code-block:: python

       output_entry = OutputEntry(name="PrintOutput")
       log_handler.config.outputs.append(output_entry)

       event_manager = EventManager(log_handler=log_handler)

       event_manager.remove_output(output_entry)
