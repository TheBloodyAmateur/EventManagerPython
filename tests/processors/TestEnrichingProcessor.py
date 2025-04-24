import inspect
import io
import os
import socket
import sys
import unittest

from EventManager import LogHandler, ProcessorEntry, OutputEntry, EventManager
from EventManager.formatters import EventCreator
from EventManager.processors import EnrichingProcessor


class TestEnrichingProcessor(unittest.TestCase):
    def setUp(self):
        self.config_path = "config/loggingConfig.json"
        self.event_manager = None
        self.original_stdout = sys.stdout
        self.output_buffer = io.StringIO()
        sys.stdout = self.output_buffer

    def tearDown(self):
        if self.event_manager:
            self.event_manager.stop_pipeline()
        sys.stdout = self.original_stdout
        print("Cleaning up test environment...")

    def get_line_number(self):
        return inspect.currentframe().f_back.f_lineno + 1

    def test_process_kv(self):
        expected_host = socket.gethostname()
        expected_ip = socket.gethostbyname(expected_host)

        enriching_processor = EnrichingProcessor(["hostname", "ip"])
        line_number = self.get_line_number()
        event = EventCreator("key-value").line_number().create()
        enriched_event = enriching_processor.process_kv(event)

        expected = f'line_number="{line_number}" hostname="{expected_host}" ip="{expected_ip}"'
        self.assertEqual(expected, enriched_event)


    def test_process_json(self):
        expected_host = socket.gethostname()
        expected_ip = socket.gethostbyname(expected_host)

        enriching_processor = EnrichingProcessor(["hostname", "ip"])
        line_number = self.get_line_number()
        event = EventCreator("json").line_number().create()
        enriched_event = enriching_processor.process_json(event)

        expected = f'{{"line_number": "{line_number}","hostname":"{expected_host}","ip":"{expected_ip}"}}'
        self.assertEqual(expected, enriched_event)

    def test_process_xml(self):
        expected_host = socket.gethostname()
        expected_ip = socket.gethostbyname(expected_host)

        enriching_processor = EnrichingProcessor(["hostname", "ip"])
        line_number = self.get_line_number()
        event = EventCreator("xml").line_number().create()
        enriched_event = enriching_processor.process_xml(event)

        expected = f'<event><line_number>{line_number}</line_number><hostname>{expected_host}</hostname><ip>{expected_ip}</ip></event>'
        self.assertEqual(expected, enriched_event)

    def test_different_parameters(self):
        os_name = os.name
        java_version = os.popen("java -version").read().strip()

        enriching_processor = EnrichingProcessor(["osName", "javaVersion"])
        line_number = self.get_line_number()
        event = EventCreator("xml").line_number().create()
        enriched_event = enriching_processor.process_xml(event)

        expected = f'<event><line_number>{line_number}</line_number><osName>{os_name}</osName><javaVersion>{java_version}</javaVersion></event>'
        self.assertEqual(expected, enriched_event)

    def test_add_processor_to_event_manager(self):
        try:
            log_handler = LogHandler("")
            log_handler.config.event.event_format = "xml"

            processor_entry = ProcessorEntry()
            processor_entry.name = "EnrichingProcessor"
            processor_entry.parameters = {"enrichingFields": ["osName", "javaVersion"]}
            log_handler.config.processors.append(processor_entry)

            output_entry = OutputEntry(name="PrintOutput")
            log_handler.config.outputs.append(output_entry)

            self.event_manager = EventManager(log_handler)
            self.event_manager.log_error_message("This is an error message")

            # Simulate waiting for events to be processed
            import time
            time.sleep(0.1)
            self.event_manager.stop_pipeline()

            event = self.output_buffer.getvalue().strip()
            self.assertTrue("<osName>" in event)
        finally:
            # Reset stdout
            sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()