#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp

# Import modules used by this controller
from models.models import *
from controllers import render_view

# MESSAGE TO READ FOR CALLER	
class MatchMessage(webapp.RequestHandler):
  def post(self):
    inputid = self.request.get('id')
    self.response.out.write("""<?xml version="1.0" encoding="UTF-8"?>
                                       <Response>
                                       <Say>""")
    if len(inputid) > 0:
      Record = CheckLog.get(inputid)	
      self.response.out.write('The condition for %s has been triggered. The condition was %s $%s. The current price is $%s, which is %s $%s.' % (Record.stock, Record.condexpcheck, Record.condprice, Record.currprice, Record.currexpcheck, Record.condprice))	
    else:
      self.response.out.write('No input was provided.')
    self.response.out.write("""</Say>
                                   </Response>""")
  # Used to test in UI
  get = post
