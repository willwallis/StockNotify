#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp

# Import modules used by this controller
from models.models import *
from controllers import render_view

# CHECK SETTINGS ADMIN
class CheckSettings(webapp.RequestHandler):
  def get(self):
    q = db.GqlQuery("SELECT * FROM CheckJobSettings ")
    if q.count() > 0:
      Settings = q.get()
    else:
      Settings = CheckJobSettings()
      Settings.detaillog = True
      Settings.put()

    template_values = {'Settings': Settings}
    self.response.out.write(render_view.full_view('', template_values, 'check_setting_body.html'))

  def post(self):
    inputid = self.request.get('id')
    Settings = CheckJobSettings.get(inputid)
    if self.request.get('detaillog') == 'true':
      Settings.detaillog = True
    else:
      Settings.detaillog = False	
    Settings.put()
    self.redirect('/admin/checksettings')
