import unittest

from EventManager.processors import MaskIPV4Address


class TestMaskIPV4Address(unittest.TestCase):

    def setUp(self):
        self.mask_ipv4_address = MaskIPV4Address(["192.168.1.0/24", "10.0.0.0/8"])

    def test_process_kv(self):
        event = 'user=JohnDoe ip="192.168.1.100" action=login'
        expected = 'user=JohnDoe ip="***.***.***.***" action=login'
        self.assertEqual(expected, self.mask_ipv4_address.process_kv(event))

    def test_process_json(self):
        event = '{"user": "JohnDoe", "ip": "10.0.0.1", "action": "login"}'
        expected = '{"user": "JohnDoe", "ip": "***.***.***.***", "action": "login"}'
        self.assertEqual(expected, self.mask_ipv4_address.process_json(event))

    def test_process_xml(self):
        event = '<event><user>JohnDoe</user><ip>192.168.1.100</ip><action>login</action></event>'
        expected = '<event><user>JohnDoe</user><ip>***.***.***.***</ip><action>login</action></event>'
        self.assertEqual(expected, self.mask_ipv4_address.process_xml(event))

    def test_process_kv_no_match(self):
        event = 'user=JohnDoe ip="172.16.0.1" action=login'
        self.assertEqual(event, self.mask_ipv4_address.process_kv(event))

    def test_process_json_no_match(self):
        event = '{"user": "JohnDoe", "ip": "172.16.0.1", "action": "login"}'
        self.assertEqual(event, self.mask_ipv4_address.process_json(event))

    def test_process_xml_no_match(self):
        event = '<event><user>JohnDoe</user><ip>172.16.0.1</ip><action>login</action></event>'
        self.assertEqual(event, self.mask_ipv4_address.process_xml(event))


if __name__ == "__main__":
    unittest.main()