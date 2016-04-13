import os
import sms_tracking
import unittest

class SmsTrackingTestCase(unittest.TestCase):

    def setUp(self):
        sms_tracking.app.config['TESTING'] = True
        self.app = sms_tracking.app.test_client()

if __name__ == '__main__':
    unittest.main()
