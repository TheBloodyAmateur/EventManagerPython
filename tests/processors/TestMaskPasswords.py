import unittest

from EventManager.processors import MaskPasswords


class TestMaskPasswords(unittest.TestCase):

    def setUp(self):
        self.mask_passwords = MaskPasswords()

    def test_process_kv(self):
        event = 'user=JohnDoe password="secret" action=login'
        expected = 'user=JohnDoe password="***" action=login'
        self.assertEqual(expected, self.mask_passwords.process_kv(event))

    def test_process_json(self):
        event = '{"user": "JohnDoe", "password": "secret", "action": "login"}'
        expected = '{"user": "JohnDoe", "password": "***", "action": "login"}'
        self.assertEqual(expected, self.mask_passwords.process_json(event))

    def test_process_xml(self):
        event = '<event><user>JohnDoe</user><password>secret</password><action>login</action></event>'
        expected = '<event><user>JohnDoe</user><password>***</password><action>login</action></event>'
        self.assertEqual(expected, self.mask_passwords.process_xml(event))

    def test_process_kv_no_password(self):
        event = 'user=JohnDoe action=login'
        self.assertEqual(event, self.mask_passwords.process_kv(event))

    def test_process_json_no_password(self):
        event = '{"user": "JohnDoe", "action": "login"}'
        self.assertEqual(event, self.mask_passwords.process_json(event))

    def test_process_xml_no_password(self):
        event = '<event><user>JohnDoe</user><action>login</action></event>'
        self.assertEqual(event, self.mask_passwords.process_xml(event))


if __name__ == "__main__":
    unittest.main()