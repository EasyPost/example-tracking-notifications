from flask import Flask, request
from twilio.rest import TwilioRestClient
import easypost

app = Flask(__name__)
app.config.from_object('config')

easypost.api_key = app.config['EASYPOST_API_KEY']
twilio_client = TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

@app.route('/easypost-webhook', methods=['POST'])
def process_webhook():
    response = request.get_json()
    #
    # Here, we check to see if the webhook is about a tracker event.
    # We'll know it is if the object is 'Event' and the description is 'tracker.updated':
    # https://www.easypost.com/tracking-guide#step2
    #

    if response['object'] == 'Event' and response['description'] == 'tracker.updated':
        event = easypost.Event.receive(request.data)
        tracker = event.result

        #
        # There are many possibilites for tailored messages with all of the
        # data returned in the EasyPost Event object.
        #
        # Here, we check the delivery status
        # and tell the customer about the latest update on their package.
        #

        message = "Hey, this is FunCompany. "

        if tracker.status == 'delivered':
            message += "Your package has arrived! "
        else:
            message += "There's an update on your package: "

        for tracking_detail in reversed(tracker.tracking_details):
            if tracking_detail.status == tracker.status:
                message += "%s says: %s in %s." % (tracker.carrier, tracking_detail.message, tracking_detail.tracking_location.city)
                break
        #
        # In a production environment, you'd want to send to the message to a specific
        # customer's phone number. Here, we just use a predefined value from settings.
        #

        twilio_client.messages.create(
            to = app.config['SMS_TO_NUMBER'],
            from_ = app.config['SMS_FROM_NUMBER'],
            body = message
        )

        return "SMS update was sent to the customer!"

if __name__ == "__main__":
    app.run(debug=True, port=12345)
