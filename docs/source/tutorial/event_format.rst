Event Format Examples
=====================

.. note::

   Keep in mind that JSON and XML are not pretty-formatted as shown in this page.
   This is done here to show some example events. The actual events are written in a single line.

Default
-------

::

    [07.02.2025 1:13:58.966 pm CET] ERROR io.github.eventmanager.EventManagerTest createDefaultEventsWithArguments 60: key="value" value="key"

- **07.02.2025 1:13:58.966 pm CET**: Timestamp
- **ERROR**: Event level
- **io.github.eventmanager.EventManagerTest**: Class from which the event was generated
- **createDefaultEventsWithArguments**: Method from which the event was generated
- **60**: Line number within the file from which it originates
- Additional arguments may follow (e.g., ``key="value"``)

CSV
---

::

    ERROR,createCSVEvents,io.github.eventmanager.EventManagerTest,07.02.2025 1:13:58.906 pm CET,141test1

JSON
----

.. code-block:: json

    {
      "luke": "skywalker",
      "level": "FATAL",
      "darth": "vader",
      "methodName": "createJSONEventsWithArguments",
      "className": "io.github.eventmanager.EventManagerTest",
      "time": "07.02.2025 1:13:58.934 pm CET",
      "lineNumber": "278"
    }

XML
---

.. code-block:: xml

    <event>
        <level>ERROR</level>
        <methodName>createXMLEvents</methodName>
        <className>io.github.eventmanager.EventManagerTest</className>
        <time>07.02.2025 1:13:58.845 pm CET</time>
        <lineNumber>195</lineNumber>
        <message>test1</message>
    </event>

Key-Value (KV)
--------------

::

    level="FATAL" methodName="createKVEvents" className="io.github.eventmanager.EventManagerTest" time="07.02.2025 1:13:58.882 pm CET" lineNumber="90" darth="vader" luke="skywalker"
