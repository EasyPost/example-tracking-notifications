require 'sinatra/base'
require 'easypost'
require 'sendgrid-ruby'
require 'tilt/erb'
require 'pry'
require 'dotenv'

class App < Sinatra::Base
  set :show_exceptions, :after_handler

  configure :development, :test do
    Dotenv.load
  end

  configure do
    EasyPost.api_key = ENV['EASYPOST_API_KEY']
    set :sendgrid, SendGrid::API.new(api_key: ENV['SENDGRID_API_KEY'])
  end

 post '/easypost-webhook' do
    response = JSON.parse(request.body.read)

    if response['object'] == 'Event' && response['description'] == 'tracker.updated'
      event = EasyPost::Event.receive(request_string)
      tracker = event.result

      message = "Hey, this is FunCompany."
      if tracker.status == 'delivered'
        message += "Your package has arrived! "
      else
        message += "There's an update on your package: "
      end

      td = tracker.tracking_details.reverse.find{|tracking_detail| tracking_detail.status == tracker.status}
      message += "#{tracker.carrier} says: #{td.message} in #{td.tracking_location.city}." if td.present?

      from = SendGrid::Email.new(email: 'test@fromaddress.com')
      subject = 'Hello World from the SendGrid Ruby Library!'
      to = SendGrid::Email.new(email: 'customer@gmail.com')
      content = SendGrid::Content.new(type: 'text/plain', value: message)
      mail = SendGrid::Mail.new(from, subject, to, content)

      output = settings.sendgrid.client.mail._("send").post(request_body: mail.to_json)

      [200, {}, "Email update was sent to the customer!"]
    else
      [200, {}, "Not a Tracker event, so nothing to do here for now..."]
    end
  end

  run! if app_file == $0
end
