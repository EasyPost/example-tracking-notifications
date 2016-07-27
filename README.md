## EasyPost Tracking Notification Examples

The EasyPost [Tracking API](https://www.easypost.com/tracking-guide) makes it simple to get EasyPost tracking updates with webhooks. These example applications show some creative ways to update you (and your customers) with the latest information on their shipments!

### Example: Sending SMS Tracking Notifications

*/sms_tracking*

This example application uses Flask, the [EasyPost Python client](https://github.com/EasyPost/easypost-python), and the [Twilio API](https://www.twilio.com/api) to send a formatted SMS message to a customer after a tracking event occurs on their shipment.

**Try this demo on your computer!**

Download the contents of this repository and use a shell to navigate to `sms_tracking/`.
Make sure you have [Python](https://www.python.org) and [pip](https://pip.pypa.io/en/stable/installing/) installed.

Since you're going to be using a test Tracker and sending SMS messages, you'll need your test API key from EasyPost (which you can find [here](https://www.easypost.com/account#/api-keys)) and an account SID, auth token, and phone number from [Twilio](https://www.twilio.com). To receive webhooks from EasyPost locally, you'll need to install [ngrok](https://ngrok.com/#download).

Run `$ pip install -r requirements.txt` to install Flask, the EasyPost Python client, and the Twilio Python library.

Rename `config-example.py` to `config.py`, and replace the placeholders with your API authorization keys. Replace `SMS_TO_NUMBER` with a number of a cell phone that can receive SMS messages.

It's time to start the app! Run `$ python sms_tracking.py`, then run `$ ngrok http 12345` in another shell to expose the app publicly through ngrok. Ngrok will give you a URL that looks something like `https://xxxxxxxx.ngrok.io`; copy it. This is the webhook URL that EasyPost will send an update to when the fake "package" has a tracker event. We need to let EasyPost know about this URL, so we'll create a new webhook with cURL:

`$ curl -X POST easypost.com/api/v2/webhooks -d 'webhook[url]=http://xxxxxxxx.ngrok.io/easypost-webhook&webhook[mode]=test' -u 'your-test-api-key:'`

(Replace "xxxxxxxx.ngrok.io" with the ngrok URL you copied, and fill in your actual EasyPost test API key).

It's showtime!  EasyPost will send us a webhook after we create a test Tracker. We use a test tracking code, "EZ2000000002" (you can find the full list of test tracking codes [here](https://www.easypost.com/docs/api#testing-specific-tracking-states)):

`$ curl -X POST https://easypost.com/v2/trackers -d 'tracker[tracking_code]=EZ2000000002' -u 'your-test-api-key:'`

Soon, you should get a customized SMS message when a shipment update occurs on the test Tracker. Awesome!

**Ideas for production-ready apps**

While this app isn't ready for production quite yet, it's a great example of what you can do with the EasyPost Tracking API. Here are some ideas for how you could extend this application:

You could:

* Notify customers if the shipment is delayed or has deliverability issues
* Alert customers with the name of the person that signed for their package
* Let a customer know when their package enters their home state, or is out for delivery
* Send email notifications in addition to SMS messages

**Unit tests**

`$ python sms_tracking_tests.py`

### Example: Sending Email Tracking Notifications

*/email_tracking*

This example application uses Sinatra, the [EasyPost Ruby client](https://github.com/EasyPost/easypost-ruby), and the [SendGrid API](https://sendgrid.com/docs/API_Reference/Web_API_v3/index.html) to send a formatted SMS message to a customer after a tracking event occurs on their shipment.

**Try this demo on your computer!**

Download the contents of this repository and use a shell to navigate to `email_tracking/`.
Make sure you have the following requirements.
### Requirements

1. A Windows or Mac computer running [Ruby](https://www.ruby-lang.org/en/)
   [Bundler](http://bundler.io/)
1. An [EasyPost account](https://www.easypost.com/signup)
1. A [SendGrid account](https://sendgrid.com/pricing/)

Since you're going to be using a test Tracker and sending Emails, you'll need your test API key from EasyPost (which you can find [here](https://www.easypost.com/account#/api-keys)) and an API key from [SendGrid](https://www.sendgrid.com). To receive webhooks from EasyPost locally, you'll need to install [ngrok](https://ngrok.com/#download).

Run `$ bundle install` to install Sinatra, the EasyPost Ruby client, and the SendGrid Ruby library.

Rename `sample.env` to `.env`, and replace the placeholders with your API authorization keys.

It's time to start the app! Run `$ ruby app.py`, then run `$ ./ngrok http 4567` in another shell to expose the app publicly through ngrok. Ngrok will give you a URL that looks something like `https://xxxxxxxx.ngrok.io`; copy it. This is the webhook URL that EasyPost will send an update to when the fake "package" has a tracker event. We need to let EasyPost know about this URL, so we'll create a new webhook with cURL:

`$ curl -X POST easypost.com/api/v2/webhooks -d 'webhook[url]=http://xxxxxxxx.ngrok.io/easypost-webhook&webhook[mode]=test' -u 'your-test-api-key:'`

(Replace "xxxxxxxx.ngrok.io" with the ngrok URL you copied, and fill in your actual EasyPost test API key).

It's showtime!  EasyPost will send us a webhook after we create a test Tracker. We use a test tracking code, "EZ2000000002" (you can find the full list of test tracking codes [here](https://www.easypost.com/docs/api#testing-specific-tracking-states)):

`$ curl -X POST https://easypost.com/v2/trackers -d 'tracker[tracking_code]=EZ2000000002' -u 'your-test-api-key:'`

Soon, you should get a customized EMAIL when a shipment update occurs on the test Tracker.

