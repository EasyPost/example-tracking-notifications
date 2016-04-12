## EasyPost Tracking Notification Examples

The EasyPost [Tracking API](https://www.easypost.com/tracking-guide) makes it super easy to manage detailed updates when tracking events occur. These example applications show some creative ways to update you (and your customers) with the latest information on their shipments!

### Example: Sending SMS with Twilio

*/sms-twilio*

This example application uses Flask, the [EasyPost Python client](https://github.com/EasyPost/easypost-python), and the [Twilio API](https://www.twilio.com/api) to send a formatted SMS message to a customer after a tracking event occurs on their shipment.

**Try out this demo on your computer!**

Download the contents of this repository and use terminal to navigate to `sms-twilio/`.
Make sure you have [Python](https://www.python.org) and [pip](https://pip.pypa.io/en/stable/installing/) installed.

Since you're going to be using a test shipment tracker and sending SMS messages, you'll need your test API key from EasyPost (which you can find [here](https://www.easypost.com/account#/api-keys)) and an account SID, auth token, and phone number from [Twilio](https://www.twilio.com). To receive webhooks from EasyPost locally, you'll need to install [ngrok](https://ngrok.com/#download).

Run `$ pip install -r requirements.txt` to install Flask, the EasyPost Python client, and the Twilio Python library.

Rename `config-example.py` to `config.py`, and replace the placeholders with your API authorization keys. Replace `SMS_TO_NUMBER` with a number of a cell phone that can receive SMS messages.

It's time to start the app! Run `$ python app.py`, then run `$ ngrok http 12345` in another terminal to expose the app publicly through ngrok. Ngrok will give you a URL that looks something like `https://something.ngrok.io`; copy it. This is the webhook URL that EasyPost will send an update to when the fake "package" has a tracker event. We need to let need to EasyPost know about this URL, so we'll create a new webhook with cURL:

`$ curl -X POST easypost.com/api/v2/webhooks -d 'webhook[url]=http://something.ngrok.io&webhook[mode]=test' -u '123:'`

(Replace "something.ngrok.io" with the ngrok URL you copied, and "123" with your EasyPost test API key).

It's showtime! Run this command to start tracking a test shipment, again replacing "123" with your test API key:

`$ curl -X POST https://easypost.com/v2/trackers -d 'tracker[tracking_code]=EZ2000000002' -u '123:'`

Soon, you should get a customized SMS message when an "update" happens on the test shipment tracker. Awesome!

**Ideas for production-ready apps**

While this app isn't ready for production quite yet, it's a great example of the versatile functionality you can harness with the EasyPost Tracking API. Here are some more cool ideas for integrations with EasyPost and the Twilio API:

You could:

* Change the wording of updates if the shipment is delayed or experiencing issues
* Send customers messages only if a property of their shipment (e.g. weight) exceeds a certain value
* Alert customers with the name of the person that signed for their package
* Let a customer know if their package reaches their home state
* Only give customers updates if the status of their delivery has changed
