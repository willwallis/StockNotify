#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp
from google.appengine.api import users

# Import modules used by this controller
from models import *

class WriteUser(webapp.RequestHandler):
  def post(self):
    inputid = self.request.get('id')
    if len(inputid) > 0: 
      userprofile = UserList.get(inputid)
    else:
      userprofile = UserList()
    userprofile.name = self.request.get('name')
    userprofile.email = self.request.get('email')
    userprofile.sms_to_number = self.request.get('sms_to_number')
    userprofile.phone_to_number = self.request.get('phone_to_number')
    userprofile.twilio_profile = self.request.get('twilio_profile')
    userprofile.put()
    TwiProf = db.GqlQuery("SELECT * FROM TwiProfile WHERE profile_name = :1 ", userprofile.twilio_profile)
    for Prof in TwiProf:
      userprofile.twilio_id = Prof.key()
    self.redirect('/admin/users')

class DeleteUser(webapp.RequestHandler):
  def post(self):
    if len(self.request.get('id')) > 0:
      userprofile = UserList.get(self.request.get('id'))
      userprofile.delete()
    self.redirect('/admin/users')
    
class WriteMyUser(webapp.RequestHandler):
  def post(self):
    inputid = self.request.get('id')
    if len(inputid) > 0: 
      userprofile = UserList.get(inputid)
    else:
      userprofile = UserList()
    userprofile.name = self.request.get('name')
    userprofile.email = self.request.get('email')
    userprofile.sms_to_number = self.request.get('sms_to_number')
    userprofile.phone_to_number = self.request.get('phone_to_number')
    userprofile.put()
    mytwiprof = TwiProfile.get(userprofile.twilio_id.key())
    mytwiprof.from_number = self.request.get('from_number')
    mytwiprof.account_sid = self.request.get('account_sid')
    mytwiprof.auth_token = self.request.get('auth_token')
    mytwiprof.put()    
    self.redirect('/myprofile')