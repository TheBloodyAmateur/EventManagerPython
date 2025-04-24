import io
import sys
import unittest

from EventManager import EventManager, LogHandler, OutputEntry, ProcessorEntry
from EventManager.filehandlers.config.regex_entry import RegexEntry
from EventManager.formatters import EventCreator, KeyValueWrapper
from EventManager.processors import RegexProcessor


class TestRegexProcessor(unittest.TestCase):
    def setUp(self):
        entry1 = RegexEntry("field1", "value1", "replacement1")
        entry2 = RegexEntry("field2", "value2", "replacement2")
        self.regex_processor = RegexProcessor([entry1, entry2])

    def test_process_kv(self):
        event = 'field1="value1" field2="value2"'
        expected = 'field1="replacement1" field2="replacement2"'
        result = self.regex_processor.process_kv(event)
        self.assertEqual(expected, result)

    def test_process_json(self):
        event = '{"field1": "value1", "field2": "value2"}'
        expected = '{"field1":"replacement1","field2":"replacement2"}'
        result = self.regex_processor.process_json(event)
        self.assertEqual(expected, result)

    def test_process_xml(self):
        event = '<field1>value1</field1><field2>value2</field2>'
        expected = '<field1>replacement1</field1><field2>replacement2</field2>'
        result = self.regex_processor.process_xml(event)
        self.assertEqual(expected, result)

    def test_add_processor_to_event_manager(self):
        original_stdout = sys.stdout
        output_buffer = io.StringIO()
        sys.stdout = output_buffer

        log_handler = LogHandler("")

        log_handler.config.event.event_format = "xml"
        output_entry = OutputEntry(name="PrintOutput")
        log_handler.config.outputs.append(output_entry)
        processor_entry = ProcessorEntry(name="RegexProcessor")
        processor_entry.parameters = {"regexEntries": [{"field_name": "field1", "regex": "value1", "replacement": "replacement1"}]}
        log_handler.config.processors.append(processor_entry)

        event_manager = EventManager(log_handler)

        # Simulate the event processing
        event = (EventCreator("xml")
                 .line_number()
                 .message("Hello, World!")
                 .arguments("args", KeyValueWrapper("field1","value1")).create())
        event_manager.log_error_message(event)

        import time
        time.sleep(1)
        event_manager.stop_pipeline()

        event = output_buffer.getvalue().strip()
        self.assertTrue('<field1>replacement1</field1>' in event)
        sys.stdout = original_stdout


if __name__ == "__main__":
    unittest.main()