#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp
from google.appengine.api import users

# Import modules used by this controller
from models.models import *
from controllers import render_view

# MY USER PROFILE
class MyProfile(webapp.RequestHandler):
  def get(self):
    UserId = users.get_current_user()
    UserProfile = db.GqlQuery("SELECT * FROM UserList WHERE goog_id = :1", UserId)
    for Profile in UserProfile:
      if Profile.twilio_id:
        MyTwi = TwiProfile.get(Profile.twilio_id.key())
      else:
        MyTwi = TwiProfile()
        MyTwi.profile_name = str(Profile.goog_id)
    	MyTwi.put()      
        Profile.twilio_profile = MyTwi.profile_name
        Profile.twilio_id = MyTwi.key()
        Profile.put()
      template_values = {'MyRecord':Profile, 'TwilioRecord':MyTwi}
      self.response.out.write(render_view.full_view('Profile', template_values, 'myprofile_body.html'))

# ALL USERS
class Users(webapp.RequestHandler):
  def get(self):
    UserList = users.get_current_user()
    TwiProfile = db.GqlQuery("SELECT * FROM TwiProfile ")
    UserProfiles = db.GqlQuery("SELECT * FROM UserList ")
    template_values = {'UserList':UserList, 'TwiProfile':TwiProfile, 'UserProfiles':UserProfiles}
    self.response.out.write(render_view.full_view('', template_values, 'users_body.html'))

    
# CREATE OR EDIT TWILIO PROFILE
class TwiProflie(webapp.RequestHandler):
  def get(self):
    inputid = self.request.get('id')
    if len(inputid) > 0: 
      MyRecord = TwiProfile.get(inputid)
    else:
      MyRecord = {}	
    template_values = {'MyRecord':MyRecord}
    self.response.out.write(render_view.full_view('', template_values, 'twi_profile_body.html'))
	
  post = get
  
# CREATE, EDIT, AND DELETE USER PROFILES
class UserProfile(webapp.RequestHandler):
  def get(self):
    inputid = self.request.get('id')
    if len(inputid) > 0: 
      MyRecord = UserList.get(inputid)
    else:
      user = users.get_current_user()
      q = db.GqlQuery("SELECT * FROM UserList WHERE goog_id = :1", user)
      if q.count() > 0:
        MyRecord = q.get()
      else:
        MyRecord = UserList()
        MyRecord.goog_id = user
    	MyRecord.put()
    TwiProfile = db.GqlQuery("SELECT * FROM TwiProfile ")

    template_values = {'MyRecord':MyRecord, 'TwiProfile':TwiProfile}
    self.response.out.write(render_view.full_view('', template_values, 'user_profile_body.html'))

  post = get
  
# LOGIN LOGIC
class LoginCheck(webapp.RequestHandler):
  def get(self):
    UserId = users.get_current_user()
    UserProfile = db.GqlQuery("SELECT * FROM UserList WHERE goog_id = :1", UserId)
    if UserProfile.count() > 0:
      #Go to List View
      self.redirect('/condlist')
    else:
      #Create new user and navigate to myprofile
      MyRecord = UserList()
      MyRecord.goog_id = UserId
      MyRecord.email = UserId.email()
      MyRecord.name = UserId.nickname()
      MyRecord.put()
      self.redirect('/myprofile')    
      