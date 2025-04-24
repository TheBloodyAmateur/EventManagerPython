import unittest

from EventManager.processors import FilterProcessor


class TestFilterProcessor(unittest.TestCase):

    def setUp(self):
        self.filter_processor = FilterProcessor(["test"])

    def test_process_kv(self):
        event = "This is a test event"
        result = self.filter_processor.process_kv(event)
        self.assertEqual("", result)

    def test_process_json(self):
        event = '{"event": "This is a test event"}'
        result = self.filter_processor.process_json(event)
        self.assertEqual("", result)

    def test_process_xml(self):
        event = "<event>This is a test event</event>"
        result = self.filter_processor.process_xml(event)
        self.assertEqual("", result)


if __name__ == "__main__":
    unittest.main()