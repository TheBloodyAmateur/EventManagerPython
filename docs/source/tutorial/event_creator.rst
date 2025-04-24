EventCreator
=================

The EventCreator is a class which provides a way to dynamically create events with custom attributes.
It is designed to be used in conjunction with the EventManager to facilitate the logging of events with specific attributes.

.. note:: The EventCreator class is not a part of the EventManager library, but it is used in conjunction with it to create events.

.. code-block:: python

   event: str = EventCreator("json").line_number().message("Hello, World!").arguments("args", KeyValueWrapper("args", "arg1")).create()
   eventManager = EventManager()
   eventManager.log_error_message(event)

The output of the above code will be a JSON string representing the event with the specified attributes:

.. code-block:: bash

   {"line_number": "25","message": "Hello, World!","args": {"args": "arg1"}}

Other examples of using the EventCreator class include:

.. code-block:: python

   event: str = EventCreator("xml").line_number().message("Hello, World!").arguments("args", KeyValueWrapper("args", "arg1")).level("CUSTOM").create()
   eventManager = EventManager()
   eventManager.log_error_message(event)

Output:

.. code-block:: xml

   <event>
       <line_number>55</line_number>
       <message>Hello, World!</message>
       <args>
           <args>arg1</args>
       </args>
       <level>CUSTOM</level>
   </event>

Some of the attributes that can be set using the EventCreator class include:

- **line_number()**: the line number to the event log.
- **class_name()**: the class name to the event log.
- **method_name()**: the method name to the event log.
- **timestamp(timestamp_format: str)**: the timestamp to the event log.
- **level(level: str)**: a custom level to the event log.
- **fatal_level()**: the fatal level to the event log.
- **error_level()**: the error level to the event log.
- **warning_level()**: the warning level to the event log.
- **info_level()**: the info level to the event log.
- **debug_level()**: the debug level to the event log.
- **exception(exception: Exception)**: an exception to the event log.
- **message(message: str)**: a message to the event log.
- **arguments(*args)**: arguments to the event log.
- **thread_id()**: the thread ID to the event log.
- **thread_name()**: the thread name to the event log.
- **hostname()**: the hostname to the event log.
- **ip_address()**: the IP address to the event log.
- **create()**: Creates and returns the event log.
