import os
import sms_tracking
import unittest
from mock import Mock, patch
import json


class SmsTrackingTestCase(unittest.TestCase):

    def setUp(self):
        sms_tracking.app.config['TESTING'] = True
        sms_tracking.app.config['SMS_FROM_NUMBER'] = '4815162342'
        sms_tracking.app.config['SMS_TO_NUMBER'] = '2432615184'

        self.app = sms_tracking.app.test_client()
        self.TEST_ROOT = os.path.realpath(os.path.dirname(__file__))

    #
    # Test that sending a GET request sends a 405 status code
    #
    def test_non_post_request(self):
        result = self.app.get('/easypost-webhook')
        self.assertEqual(result.status_code, 405)

    #
    # Test that if the JSON sent is not an Event object, the script still returns 200
    #
    def test_non_event_request(self):
        result = self.app.post(
            '/easypost-webhook',
            data=json.dumps(dict(object='FakeObject', description='fake.description')),
            content_type='application/json'
        )
        self.assertEqual(result.status_code, 200)

    #
    # Tests what happens if JSON is sent that indicates a package with "delivered" status
    #
    @patch("sms_tracking.TwilioRestClient")
    def test_delivered_succeeds(self, TwilioRestClient):
        mock_messages = Mock()
        mock_client = Mock(messages=mock_messages)
        TwilioRestClient.return_value = mock_client

        delivered_data = open(os.path.join(self.TEST_ROOT, 'test_data', 'delivered.json')).read()
        result = self.app.post(
            '/easypost-webhook',
            data=delivered_data,
            content_type='application/json'
        )

        self.assertEqual(result.status_code, 200)

        mock_messages.create.assert_called_once_with(
            from_='4815162342',
            to='2432615184',
            body="Hey, this is FunCompany. Your package has arrived! UPS says: DELIVERED in SAN FRANCISCO."
        )

    #
    # Tests what happens if JSON is sent that indicates a package with "in_transit" status
    #
    @patch("sms_tracking.TwilioRestClient")
    def test_in_transit_succeeds(self, TwilioRestClient):
        mock_messages = Mock()
        mock_client = Mock(messages=mock_messages)
        TwilioRestClient.return_value = mock_client

        in_transit_data = open(os.path.join(self.TEST_ROOT, 'test_data', 'in_transit.json')).read()
        result = self.app.post(
            '/easypost-webhook',
            data=in_transit_data,
            content_type='application/json'
        )

        self.assertEqual(result.status_code, 200)

        mock_messages.create.assert_called_once_with(
            from_='4815162342',
            to='2432615184',
            body="Hey, this is FunCompany. There's an update on your package: UPS says: ARRIVAL SCAN in SAN FRANCISCO."
        )


if __name__ == '__main__':
    unittest.main()
