import io
import socket
import sys
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from EventManager.event_manager import EventManager
from EventManager.filehandlers.config.output_entry import OutputEntry
from EventManager.filehandlers.config.processor_entry import ProcessorEntry
from EventManager.filehandlers.config.regex_entry import RegexEntry
from EventManager.filehandlers.config.socket_entry import SocketEntry
from EventManager.filehandlers.log_handler import LogHandler
from EventManager.formatters.key_value_wrapper import KeyValueWrapper


def wait_for_events():
    """
    A simple function to wait for events to be processed, in order to prevent timeouts due to asynchronous processing.
    """
    time.sleep(0.1)


class TestEventManager(unittest.TestCase):
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

    def assert_log_contains(self, expected_text):
        wait_for_events()
        log_path = Path(
            self.event_manager._log_handler.config.log_file.file_path + self.event_manager._log_handler.current_file_name)
        log_lines = log_path.read_text(encoding="utf-8").splitlines()
        self.assertTrue(any(expected_text in line for line in log_lines))

    def test_create_instance(self):
        log_handler = LogHandler(self.config_path)
        self.event_manager = EventManager(log_handler)

    def test_create_default_events(self):
        log_handler = LogHandler(self.config_path)
        log_handler.config.event.event_format = "default"
        self.event_manager = EventManager(log_handler)

        self.event_manager.log_error_message("This is an error message")
        self.event_manager.log_warning_message("This is an warning message")
        self.event_manager.log_fatal_message("This is a fatal message")

        wait_for_events()

        self.assertTrue(log_handler.check_if_log_file_exists())
        self.assert_log_contains("error message")
        self.assert_log_contains("warning message")
        self.assert_log_contains("fatal message")

    def test_create_default_events_with_arguments(self):
        log_handler = LogHandler(self.config_path)
        log_handler.config.event.event_format = "default"
        self.event_manager = EventManager(log_handler)

        self.event_manager.log_warning_message(
            KeyValueWrapper("gisela", "brünhilde"),
            KeyValueWrapper("detlef", "herzig")
        )

        wait_for_events()

        self.assertTrue(log_handler.check_if_log_file_exists())
        self.assert_log_contains("gisela=\"brünhilde\"")
        self.assert_log_contains("detlef=\"herzig\"")

    def test_create_kv_events(self):
        log_handler = LogHandler(self.config_path)
        log_handler.config.event.event_format = "kv"
        self.event_manager = EventManager(log_handler)

        self.event_manager.log_error_message(
            KeyValueWrapper("key", "value"),
            KeyValueWrapper("value", "key")
        )

        wait_for_events()

        self.assertTrue(log_handler.check_if_log_file_exists())
        self.assert_log_contains("key=\"value\"")

    def test_create_json_events(self):
        log_handler = LogHandler(self.config_path)
        log_handler.config.event.event_format = "json"

        self.event_manager = EventManager(log_handler)
        self.event_manager.log_error_message("test1")

        wait_for_events()

        self.assertTrue(log_handler.check_if_log_file_exists())
        self.assert_log_contains('"message": "test1"')

    def test_console_output(self):
        log_handler = LogHandler(self.config_path)
        output_entry = OutputEntry(name="PrintOutput")
        log_handler.config.outputs.append(output_entry)

        self.event_manager = EventManager(log_handler)
        self.event_manager.log_error_message("This is an error message")

        wait_for_events()

        self.assertIn("This is an error message", self.output_buffer.getvalue())

    def test_monitor(self):
        log_handler = LogHandler(self.config_path)
        log_handler.config.event.event_format = "json"
        output_entry = OutputEntry(name="PrintOutput")
        log_handler.config.outputs.append(output_entry)

        self.event_manager = EventManager(log_handler)
        self.event_manager.monitor("test", 100, lambda: time.sleep(0.2))

        wait_for_events()

        self.assertIn("Operation test took", self.output_buffer.getvalue())

    def test_add_and_remove_output(self):
        log_handler = LogHandler(self.config_path)
        log_handler.config.event.event_format = "json"
        output_entry = OutputEntry(name="PrintOutput")
        log_handler.config.outputs.append(output_entry)

        self.event_manager = EventManager(log_handler)
        self.event_manager.log_error_message("This is an error message")
        wait_for_events()

        self.event_manager.remove_output(OutputEntry("PrintOutput", None))

        test = self.output_buffer.getvalue().strip()
        self.assertTrue("\"message\": \"This is an error message\"" in test)

    def test_add_processor_and_verify_output(self):
        log_handler = LogHandler(self.config_path)
        log_handler.config.event.event_format = "json"
        output_entry = OutputEntry(name="PrintOutput")
        log_handler.config.outputs.append(output_entry)

        self.event_manager = EventManager(log_handler)
        processor_entry = ProcessorEntry(name="RegexProcessor", parameters={
            "regexEntries": [RegexEntry("level", "ERROR", "KETCHUP")]
        })
        self.event_manager.add_processor(processor_entry)
        self.event_manager.log_error_message("This is an error message")

        wait_for_events()

        self.assertIn('"level":"KETCHUP"', self.output_buffer.getvalue())

    def test_remove_processor_and_verify_output(self):
        log_handler = LogHandler(self.config_path)
        log_handler.config.event.event_format = "json"
        output_entry = OutputEntry(name="PrintOutput")
        log_handler.config.outputs.append(output_entry)

        self.event_manager = EventManager(log_handler)
        processor_entry = ProcessorEntry(name="RegexProcessor", parameters={
            "regexEntries": [RegexEntry("level", "ERROR", "KETCHUP")]
        })
        self.event_manager.add_processor(processor_entry)

        wait_for_events()

        self.event_manager.log_error_message("This is an error message")

        wait_for_events()

        self.event_manager.remove_processor("RegexProcessor")

        self.assertIn('"level":"KETCHUP"', self.output_buffer.getvalue())

    def test_sample_processor(self):
        log_handler = LogHandler(self.config_path)
        log_handler.config.event.event_format = "json"
        output_entry = OutputEntry(name="PrintOutput")
        log_handler.config.outputs.append(output_entry)

        processor_entry = ProcessorEntry(name="SampleProcessor", parameters={"sampleSize": 2})
        log_handler.config.processors.append(processor_entry)

        self.event_manager = EventManager(log_handler)

        for i in range(10):
            self.event_manager.log_error_message(f"This is a test message {i}")

        wait_for_events()

        output = self.output_buffer.getvalue()
        for i in range(1, 10, 2):
            self.assertIn(f"This is a test message {i}", output)

    def test_filter_processor(self):
        log_handler = LogHandler(self.config_path)
        log_handler.config.event.event_format = "json"
        output_entry = OutputEntry(name="PrintOutput")
        log_handler.config.outputs.append(output_entry)
        processor_entry = ProcessorEntry(name="FilterProcessor", parameters={"termToFilter": ["test_message"]})
        log_handler.config.processors.append(processor_entry)

        self.event_manager = EventManager(log_handler)
        self.event_manager.log_error_message("This is a test_message")
        self.event_manager.log_error_message("This is a message without the term")

        wait_for_events()

        output = self.output_buffer.getvalue()
        self.assertIn("This is a message without the term", output)
        self.assertNotIn("This is a test message", output)

    def test_socket_output(self):
        log_handler = LogHandler(self.config_path)
        socket_entry = OutputEntry(name="SocketOutput", parameters={
            "socketSettings": [SocketEntry("localhost", 6000)]
        })

        self.event_manager = EventManager(log_handler)
        self.event_manager.add_output(socket_entry)

        server = socket.socket()
        server.bind(("localhost", 6000))
        server.listen(1)
        server.settimeout(5)  # Set a timeout to prevent indefinite blocking

        def handle_connection():
            try:
                conn, _ = server.accept()
                data = conn.recv(1024).decode()
                conn.close()
                return data
            except socket.timeout:
                return ""

        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(handle_connection)

                for _ in range(1000):
                    self.event_manager.log_error_message("This is an error message")

                wait_for_events()
                received = future.result(timeout=5)
                self.assertIn("This is an error message", received)
        finally:
            server.close()


if __name__ == '__main__':
    unittest.main()
