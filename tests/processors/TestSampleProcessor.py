import unittest

from EventManager.processors import SampleProcessor


class TestSampleProcessor(unittest.TestCase):

    def setUp(self):
        self.sample_processor = SampleProcessor(5)

    def test_process_kv(self):
        key_value_event = "key=value"
        result = self.sample_processor.process_kv(key_value_event)
        self.assertEqual("", result)

    def test_process_json(self):
        event = '{"event": "This is a test event"}'
        result = self.sample_processor.process_json(event)
        self.assertEqual("", result)

    def test_process_xml(self):
        event = "<event>This is a test event</event>"
        result = self.sample_processor.process_xml(event)
        self.assertEqual("", result)

    def test_process_text(self):
        json_event = '{"event": "This is a test event"}'
        event = ""

        for _ in range(5):
            event = self.sample_processor.process_json(json_event)

        self.assertEqual(json_event, event)


if __name__ == "__main__":
    unittest.main()