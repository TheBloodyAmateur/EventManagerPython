Tutorial
========

This tutorial walks you through a basic setup of EventManager in a Python project.

Basic Usage
----------------
To get started with EventManager, you need to import the necessary classes and create an instance of
the `EventManager` class. The following example demonstrates how to set up a basic event manager to log a warning message:
   .. code-block:: python

      from EventManager import event_manager

      event_manager = EventManager(config_path="/path/to/config/file.json")
      event_manager.log_error_message("Hello, EventManager!")
      event_manager.log_warning_message("This is a warning message.")
      event_manager.stop_pipeline()

Another example shows how to set up a basic event manager with a custom LogHandler object to set the log level and format:
    .. code-block:: python

        from EventManager import event_manager, LogHandler

        log_handler = LogHandler(config_path="/path/to/config/file.json")
        log_handler.config.event.event_format = "json"
        event_manager = EventManager(log_handler)
        event_manager.log_warning_message("This is a warning message.")
        event_manager.stop_pipeline()

See the main page for details on top-level APIs.