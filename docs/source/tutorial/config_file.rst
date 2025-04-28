Configuration Specification
===========================

Here is an example of how a configuration file may look:

.. code-block:: json

   {
     "event": {
       "debuggingMode": false,
       "informationalMode": false,
       "timeFormat": "dd.MM.yyyy h:mm:ss.SSS a z",
       "eventFormat": "kv"
     },
     "logFile": {
       "filePath": "/tmp/",
       "fileName": "application",
       "fileExtension": ".log"
     },
     "logRotateConfig": {
       "maxSizeInKB": 131072,
       "rotationPeriodInSeconds": 10,
       "compressionFormat": "gzip"
     },
     "internalEvents": {
       "filePath": "/tmp/",
       "fileName": "internal",
       "fileExtension": ".log",
       "enabled": "true"
     },
     "processors": [
       {
         "name": "MaskIPV4Address",
         "parameters": {
           "excludeRanges": ["192.168.1.0/24", "10.0.0.0/8"]
         }
       },
       {
         "name": "MaskPasswords",
         "parameters": {}
       }
     ],
     "outputs": [
       {
         "name": "PrintOutput",
         "parameters": {}
       }
     ]
   }

Event
-----

The ``event`` object defines settings about the events themselves:

- ``debuggingMode``: Enable or disable the debugging mode and therefore save the debug events (Default: ``false``)
- ``informationalMode``: Enable or disable the informational mode and therefore save the info events (Default: ``false``)
- ``printAndSaveToFile``: An option to both save the events in a file, but also print them out in the console (Default: ``false``)
- ``printToConsole``: If enabled only prints the events in the console and doesn't write them to a log file (Default: ``false``)
- ``timeFormat``: The time format specified for the events. If invalid, EventManager falls back to a default. (Default: ``"dd.MM.yyyy h:mm:ss.SSS a z"``)
- ``eventFormat``: Specifies the format of the events. Options include ``csv``, ``xml``, ``json``, ``kv`` (Key-Value) or the default format. (Default: ``default``)

Log File
--------

The ``logFile`` object defines basic settings for the log file:

- ``filePath``: The file path of the log file (Default: ``"/tmp/"``)
- ``fileName``: The name of the log file (Default: ``"application"``)
- ``fileExtension``: The file extension of the log file (Default: ``".log"``)

Log Rotation
------------

The ``logRotateConfig`` specifies configuration about the log rotation:

- ``maxSizeInKB``: The maximum size a log file can be (in KB) before it gets rotated (Default: ``131072``)
- ``rotationPeriodInSeconds``: The period after which a file should be rotated (in seconds) (Default: ``10``)
- ``compressionFormat``: The compression format used for log files (Default: ``gzip``)

Internal Events
---------------

The ``internalEvents`` object defines settings for internal logging:

- ``filePath``: Path of the internal log file (Default: ``"/tmp/"``)
- ``fileName``: Name of the internal log file (Default: ``"internal"``)
- ``fileExtension``: Extension of the internal log file (Default: ``".log"``)
- ``enabled``: Whether to enable internal logs (Default: ``true``)

Processors
----------

The ``processors`` list specifies transformations or enrichments for events:

Each object defines a processor by:

- ``name``: Class name of the processor
- ``parameters``: Processor-specific parameters

The default processor is ``MaskPasswords``.

Outputs
-------

The ``outputs`` list defines how and where events are output:

Each object defines an output by:

- ``name``: Class name of the output
- ``parameters``: Output-specific parameters

The default output is ``LogOutput``.

Partial Configuration
---------------------

You can specify only the parts of the configuration that need to be overridden. For example, if only the log file settings need customization:

.. code-block:: json

   {
     "logFile": {
       "filePath": "/var/log/myApplication/",
       "fileName": "myApplication",
       "fileExtension": ".differentExtension"
     }
   }

The remaining values will be loaded from defaults.

Set Configuration During Runtime
--------------------------------

It is possible to set and update the configuration during runtime:

.. code-block:: python

   logHandler = LogHandler("/etc/myApplication/loggingConfig.json")
   eventManager = EventManager(logHandler)

