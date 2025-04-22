Tutorial
========

This tutorial walks you through a basic setup of EventManager in a Python project.

1. **Install the package**

   .. code-block:: bash

      pip install EventManager

2. **Basic Usage**

   .. code-block:: python

      from EventManager import event_manager

      event_manager.log_error_message("Hello, EventManager!")
      event_manager.log_warning_message("This is a warning message.")
      event_manager.stop_pipeline()

3. **Advanced Setup**

   You can configure outputs, add processors, and switch to JSON or CSV formatting.

See :doc:`top_level` for details on top-level APIs.