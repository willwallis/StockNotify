#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp
from google.appengine.api import users

# Import modules used by this controller
from models import *

# Write Twilio record for create or update
class WriteTwilio(webapp.RequestHandler):
  def post(self):
    inputid = self.request.get('id')
    if len(inputid) > 0: 
      twiprofile = TwiProfile.get(inputid)
    else:
      twiprofile = TwiProfile()
    twiprofile.profile_name = self.request.get('profile_name')
    twiprofile.from_number = self.request.get('from_number')
    twiprofile.account_sid = self.request.get('account_sid')
    twiprofile.auth_token = self.request.get('auth_token')
    twiprofile.put()
    self.redirect('/admin/users')

# Delete Twilio record
class DeleteTwilio(webapp.RequestHandler):
  def post(self):
    if len(self.request.get('id')) > 0:
      twiprofile = TwiProfile.get(self.request.get('id'))
      twiprofile.delete()
    self.redirect('/admin/users')