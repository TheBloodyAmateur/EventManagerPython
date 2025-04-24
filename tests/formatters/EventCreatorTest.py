import socket
import threading
import unittest
import inspect

from EventManager.formatters import EventCreator, KeyValueWrapper


class TestEventCreator(unittest.TestCase):
    def get_line_number(self):
        return inspect.currentframe().f_back.f_lineno+1

    def test_json_event_one(self):
        line = self.get_line_number()
        event = EventCreator("json").line_number().create()
        self.assertEqual(f'{{"line_number": "{line}"}}', event)

    def test_json_event_two(self):
        line = self.get_line_number()
        event = EventCreator("json").line_number().message("Hello, World!").create()
        self.assertEqual(event, f'{{"line_number": "{line}","message": "Hello, World!"}}')

    def test_json_event_three(self):
        line = self.get_line_number()
        event = EventCreator("json").line_number().message("Hello, World!").arguments("args", KeyValueWrapper("args", "arg1")).create()
        self.assertEqual(f'{{"line_number": "{line}","message": "Hello, World!","args": {{"args": "arg1"}}}}', event)

    def test_json_custom_log_level(self):
        line = self.get_line_number()
        event = EventCreator("json").line_number().message("Hello, World!").arguments(KeyValueWrapper("args", "arg1")).level("CUSTOM").create()
        self.assertEqual(f'{{"line_number": "{line}","message": "Hello, World!","args": {{"args": "arg1"}},"level": "CUSTOM"}}', event)

    def test_json_info_log_level(self):
        line = self.get_line_number()
        event = EventCreator("json").line_number().message("Hello, World!").arguments("args", KeyValueWrapper("args", "arg1")).level("INFO").create()
        self.assertEqual(event, f'{{"line_number": "{line}","message": "Hello, World!","args": {{"args": "arg1"}},"level": "INFO"}}')

    def test_xml_event_one(self):
        line = self.get_line_number()
        event = EventCreator("xml").line_number().create()
        self.assertEqual(event, f"<event><line_number>{line}</line_number></event>")

    def test_xml_event_two(self):
        line = self.get_line_number()
        event = EventCreator("xml").line_number().message("Hello, World!").create()
        self.assertEqual(event, f"<event><line_number>{line}</line_number><message>Hello, World!</message></event>")

    def test_xml_event_three(self):
        line = self.get_line_number()
        event = EventCreator("xml").line_number().message("Hello, World!").arguments("args", KeyValueWrapper("args", "arg1")).create()
        self.assertEqual(f"<event><line_number>{line}</line_number><message>Hello, World!</message><args><args>arg1</args></args></event>",event)

    def test_xml_custom_log_level(self):
        line = self.get_line_number()
        event = EventCreator("xml").line_number().message("Hello, World!").arguments("args", KeyValueWrapper("args", "arg1")).level("CUSTOM").create()
        self.assertEqual(event, f"<event><line_number>{line}</line_number><message>Hello, World!</message><args><args>arg1</args></args><level>CUSTOM</level></event>")

    def test_xml_info_log_level(self):
        line = self.get_line_number()
        event = EventCreator("xml").line_number().message("Hello, World!").arguments("args", KeyValueWrapper("args", "arg1")).level("INFO").create()
        self.assertEqual(event, f"<event><line_number>{line}</line_number><message>Hello, World!</message><args><args>arg1</args></args><level>INFO</level></event>")

    def test_csv_event_one(self):
        line = self.get_line_number()
        event = EventCreator("csv").line_number().create()
        self.assertEqual(event, f"{line}")

    def test_csv_event_two(self):
        line = self.get_line_number()
        event = EventCreator("csv").line_number().message("Hello World!").create()
        self.assertEqual(event, f"{line},Hello World!")

    def test_csv_event_three(self):
        line = self.get_line_number()
        event = EventCreator("csv").line_number().message("Hello World!").arguments(KeyValueWrapper("args", "arg1")).create()
        self.assertEqual(event, f"{line},Hello World!,arg1")

    def test_csv_custom_log_level(self):
        line = self.get_line_number()
        event = EventCreator("csv").line_number().message("Hello World!").arguments(KeyValueWrapper("args", "arg1")).level("CUSTOM").create()
        self.assertEqual(event, f"{line},Hello World!,arg1,CUSTOM")

    def test_csv_info_log_level(self):
        line = self.get_line_number()
        event = EventCreator("csv").line_number().message("Hello World!").arguments(KeyValueWrapper("args", "arg1")).level("INFO").create()
        self.assertEqual(event, f"{line},Hello World!,arg1,INFO")

    def test_hostname(self):
        hostname = socket.gethostname()
        line = self.get_line_number()
        event = EventCreator("json").line_number().hostname().create()
        self.assertEqual(f'{{"line_number": "{line}","hostname": "{hostname}"}}', event)

    def test_ip_address(self):
        ip = socket.gethostbyname(socket.gethostname())
        line = self.get_line_number()
        event = EventCreator("json").line_number().ip_address().create()
        self.assertEqual(f'{{"line_number": "{line}","ip_address": "{ip}"}}', event)

    def test_thread_name(self):
        thread_name = threading.current_thread().name
        line = self.get_line_number()
        event = EventCreator("json").line_number().thread_name().create()
        self.assertEqual(f'{{"line_number": "{line}","thread_name": "{thread_name}"}}', event)
