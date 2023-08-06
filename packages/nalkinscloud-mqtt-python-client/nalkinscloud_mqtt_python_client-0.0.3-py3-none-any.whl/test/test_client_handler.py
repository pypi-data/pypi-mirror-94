import unittest

from nalkinscloud_mqtt_python_client.mqtt_handler import MQTTClient, is_valid_topic

valid_topic = 'some/valid/topic'
invalid_topic = 'invalid/topic'
invalid_topic2 = '//'
empty_topic = ''


class FunctionsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_valid_topic(self):
        self.assertTrue(is_valid_topic(valid_topic))
        self.assertFalse(is_valid_topic(invalid_topic))
        self.assertFalse(is_valid_topic(invalid_topic2))
        self.assertFalse(is_valid_topic(empty_topic))
        self.assertFalse(is_valid_topic(None))


class MqttHandlerTest(unittest.TestCase):

    def setUp(self):
        self.device_id = 'test_dht_simulator'
        self.device_pass = 'nalkinscloud'
        self.device_type = 'dht'
        self.device_qos = 1
        self.subscription_update = 'update_now'

        # Define mqtt_client for current test case
        self.mqtt_client = MQTTClient(broker_host='localhost', broker_port=1883,
                                      broker_cert=None, broker_tls=False)

        self.mqtt_client.init_device(device_id=self.device_id,
                                     device_password=self.device_pass,
                                     device_type=self.device_type,
                                     qos=self.device_qos,
                                     subscription_update=self.subscription_update)

    def test_init_device(self):
        self.assertEqual('test_dht_simulator', self.mqtt_client._device_id)

    def test_get_mqtt_client(self):
        self.assertEqual(self.mqtt_client.get_mqtt_client(), self.mqtt_client._mqtt_client)

    def test_set_lwt(self):
        self.assertFalse(self.mqtt_client._mqtt_client._will)
        self.mqtt_client.set_lwt(device_id=self.device_id,
                                 device_type=self.device_type,
                                 qos=self.device_qos,
                                 is_retained=True)
        self.assertTrue(self.mqtt_client._mqtt_client._will)

    def test_connect(self):
        # Try connecting to localhost (while no mqtt server is running)
        self.assertRaises(Exception, self.mqtt_client.connect())


if __name__ == '__main__':
    unittest.main()
