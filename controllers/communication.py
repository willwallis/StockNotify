#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp
from google.appengine.api import mail

# Import modules used by this controller
from models.models import *
from twilio.rest import TwilioRestClient

# Gets communications profile	  
def get_profile(requestor):
    UserProfile = db.GqlQuery("SELECT * FROM UserList WHERE goog_id = :1 ", requestor)
    CallProfile={}
    for Profile in UserProfile:
      TwiProfile = db.GqlQuery("SELECT * FROM TwiProfile where profile_name = :1", Profile.twilio_profile)
      CallProfile = {'to_email':Profile.email}
      CallProfile.update({'to_sms':Profile.sms_to_number})
      CallProfile.update({'to_phone':Profile.phone_to_number})
    for Twilio in TwiProfile:
      CallProfile.update({'from_phone':Twilio.from_number})
      CallProfile.update({'account_sid':Twilio.account_sid})
      CallProfile.update({'auth_token':Twilio.auth_token})
    return (CallProfile)
	
# Sends notification email	  
def notify_email(requestor, message_text, stock):
    ProfDetails = get_profile(requestor)
    to_address = ProfDetails['to_email']	  
    if to_address != "":
        message = mail.EmailMessage(sender="Stock Notifier <example@gmail.com>",
                            subject="Stock Notifier Triggered: %s" % stock)
        message.to = to_address
        message.body = message_text
        message.send()

# Send notification SMS		
def notify_sms(requestor, message_text):
    ProfDetails = get_profile(requestor)
    to_number = ProfDetails['to_sms']	  
    account_sid = ProfDetails['account_sid']
    auth_token = ProfDetails['auth_token']
    from_number = ProfDetails['from_phone']
    SMSclient = TwilioRestClient(account_sid, auth_token)
    SMSmessage = SMSclient.sms.messages.create(to=to_number, from_=from_number, body=message_text)

# Make a notification phone Call
def make_call(requestor, message_url):
    ProfDetails = get_profile(requestor)
    to_number = ProfDetails['to_phone']	  
    account_sid = ProfDetails['account_sid']
    auth_token = ProfDetails['auth_token']
    from_number = ProfDetails['from_phone']
    Callclient = TwilioRestClient(account_sid, auth_token)
 
    # Make the call
    call = Callclient.calls.create(to=to_number,  # Any phone number
                               from_=from_number, # Must be a valid Twilio number
                               url=message_url)
