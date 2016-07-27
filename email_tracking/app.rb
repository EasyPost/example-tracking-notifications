require 'sinatra/base'
require 'easypost'
require 'sendgrid-ruby'
require 'tilt/erb'
require 'pry'
require 'dotenv'

include SendGrid

class App < Sinatra::Base
  set :show_exceptions, :after_handler

  configure :development, :test do
    Dotenv.load
  end

  configure do
    EasyPost.api_key = ENV['EASYPOST_API_KEY']
    set :sendgrid_key, SendGrid::API.new(api_key: ENV['SENDGRID_API_KEY'])
  end


 post '/easypost-webhook' do
    sendgrid = settings.sendgrid_key
    request.body.rewind
    request_string = request.body.read.to_s
    response = JSON.parse(request_string)

    if response['object'] == 'Event' && response['description'] == 'tracker.updated'
      event = EasyPost::Event.receive(request_string)
      tracker = event.result

      @message = "Hey, this is FunCompany."
      if tracker.status == 'delivered'
        @message += "Your package has arrived! "
      else
        @message += "There's an update on your package: "
      end

      tracker.tracking_details.reverse.each do |tracking_detail|
        if tracking_detail.status == tracker.status
          @message += "%s says: %s in %s." % [tracker.carrier,tracking_detail.message,tracking_detail.tracking_location.city]
        end
        break
      end

      from = Email.new(email: 'test@fromaddress.com')
      subject = 'Hello World from the SendGrid Ruby Library!'
      to = Email.new(email: 'customer@gmail.com')
      content = Content.new(type: 'text/plain', value: @message)
      mail = Mail.new(from, subject, to, content)

      output = sendgrid.client.mail._("send").post(request_body: mail.to_json)

      return "Email update was sent to the customer!"
    else
        return "Not a Tracker event, so nothing to do here for now..."
    end
  end

  run! if app_file == $0
end
