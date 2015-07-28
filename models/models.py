#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import db

# DATA MODELS
# These classes define the data objects that you will be able to store in AppEngine's data store.

# Model for Condition database
class Condition(db.Model):
  """Models an individual Condition entry with an author, stock, status, price, expression, and date."""
  author = db.UserProperty()
  stock = db.StringProperty()
  status = db.StringProperty()
  price = db.FloatProperty()
  expcheck = db.StringProperty()
  email = db.BooleanProperty(default=False)
  phone = db.BooleanProperty(default=False)
  sms = db.BooleanProperty(default=False)
  date = db.DateTimeProperty(auto_now_add=True)

# Model for CheckRuns database
class CheckRun(db.Model):
  """Models records an entry for each checklog run"""
  date = db.DateTimeProperty(auto_now_add=True)
  condcount = db.IntegerProperty()
  matchcount = db.IntegerProperty() 
  
# Model for CheckLogs database
class CheckLog(db.Model):
  """Models log record entry with stock, condition, conditional price, current price, current condition and match"""
  stock = db.StringProperty()
  condexpcheck = db.StringProperty()
  condprice = db.FloatProperty()
  currprice = db.FloatProperty() 
  currexpcheck = db.StringProperty()
  currmatch = db.BooleanProperty() 
  email = db.BooleanProperty()
  phone = db.BooleanProperty()
  sms = db.BooleanProperty()
  requestor = db.UserProperty()
  condition = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)

# Model for US Stock List. http://www.nasdaq.com/screening/company-list.aspx for updates
class USStockList(db.Model):
  """Models contain list of US stocks from NYSE, AMEX & NASDAQ"""
  exchange = db.StringProperty()
  symbol = db.StringProperty()
  name = db.StringProperty()
  comboname = db.StringProperty()
 
# Model for User Details 
class UserList(db.Model):
  """Models contains details for a user"""
  goog_id = db.UserProperty()
  name = db.StringProperty()
  email = db.StringProperty()
  sms_to_number = db.StringProperty()
  phone_to_number = db.StringProperty()
  twilio_profile = db.StringProperty()
  twilio_id = db.ReferenceProperty()
  
# Model for Twilio Tokens
class TwiProfile(db.Model):
  """Models contains details for a twilio profile"""
  profile_name = db.StringProperty()
  from_number = db.StringProperty()
  account_sid = db.StringProperty()
  auth_token = db.StringProperty()

# Model for Check Job Settings
class CheckJobSettings(db.Model):
  """Models contains settings for the Check Job"""
  detaillog = db.BooleanProperty()