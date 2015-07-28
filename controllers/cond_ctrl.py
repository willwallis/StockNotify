#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp
from google.appengine.api import users

# Import modules used by this controller
from models.models import *
from controllers import render_view

# The condition list
class List(webapp.RequestHandler):
  def get(self):
    ListType = self.request.get('listtype')
    if ListType == 'allsorts':
      Conditions = db.GqlQuery("SELECT * "
                              "FROM Condition "
                              "ORDER BY date DESC",
                              )
    else:
      QueryUser = users.get_current_user()
      Conditions = db.GqlQuery("SELECT * "
                              "FROM Condition "
                              "WHERE author = :1 "
                              "ORDER BY date DESC",
                              QueryUser)
    template_values = {'Conditions': Conditions}
    self.response.out.write(render_view.full_view('List', template_values, 'list_body.html'))

# The condition create form
class Create(webapp.RequestHandler):
  def get(self):
    QueryUser = users.get_current_user()
    Conditions = db.GqlQuery("SELECT * "
                            "FROM Condition "
                            "WHERE author = :1 "
                            "ORDER BY date DESC",
                            QueryUser)
    template_values = {'Conditions': Conditions}
    self.response.out.write(render_view.full_view('Create', template_values, 'create_cond_body.html'))

# The condition edit form
class Edit(webapp.RequestHandler):
  def post(self):
    inputid = self.request.get('id')
    MyRecord = Condition.get(inputid)
    template_values = {'MyRecord': MyRecord}
    self.response.out.write(render_view.full_view('List', template_values, 'edit_cond_body.html'))

  get = post
