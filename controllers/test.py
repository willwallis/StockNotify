#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp

# Import modules used by this controller
from controllers import render_view

# CLASS TO SUPPORT ABOUT PAGE
class Test(webapp.RequestHandler):
  def get(self):
    template_values = {}
    self.response.out.write(render_view.full_view('', template_values, 'test_body.html'))
