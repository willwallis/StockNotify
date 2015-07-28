#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp

# Import modules used by this controller
from models.models import *
from controllers import render_view

# CHECK RUN LOGS
class CheckRuns(webapp.RequestHandler):
  def get(self):
    query = db.GqlQuery("SELECT * FROM CheckRun "
	                 "ORDER BY date DESC" )
    PageTitle = "Check Runs"  
    myAction = self.request.get('action')
    if myAction == 'next':
      RecordCount = query.count()
      FetchMax = int(self.request.get('FetchLocation')) + 15
      if FetchMax < RecordCount:
        FetchLocation = FetchMax
      else:
        FetchLocation = int(self.request.get('FetchLocation'))  
    elif myAction == 'previous':
      FetchLocation = int(self.request.get('FetchLocation')) - 15
      if FetchLocation < 0:
        FetchLocation = 0
    else:
      FetchLocation = 0
  
    CheckRuns = query.fetch(15, FetchLocation)
    template_values = {'CheckRuns': CheckRuns, 'FetchLocation': FetchLocation, 'PageTitle':PageTitle}
    self.response.out.write(render_view.full_view('', template_values, 'check_runs_body.html'))
 	 
  post = get
	
# CHECK DETAIL LOGS
class CheckLogs(webapp.RequestHandler):
  def get(self):
    if len(self.request.get('RunKey')) > 0:
      ParentRun = self.request.get('RunKey')
      query = db.GqlQuery("SELECT * FROM CheckLog WHERE ANCESTOR IS :1 "
	                 "ORDER BY date DESC", ParentRun)
      PageTitle = 'Check Logs: Run No. %s ' % CheckRun.get(ParentRun).key().id()
    else:
      query = db.GqlQuery("SELECT * FROM CheckLog "
	                 "ORDER BY date DESC" )
      PageTitle = 'Check Logs' 
      ParentRun = ''
	  
    myAction = self.request.get('action')
    if myAction == 'next':
      RecordCount = query.count()
      FetchMax = int(self.request.get('FetchLocation')) + 15
      if FetchMax < RecordCount:
        FetchLocation = FetchMax
      else:
        FetchLocation = int(self.request.get('FetchLocation'))  
    elif myAction == 'previous':
      FetchLocation = int(self.request.get('FetchLocation')) - 15
      if FetchLocation < 0:
        FetchLocation = 0
    else:
      FetchLocation = 0
    
    CheckLogs = query.fetch(15, FetchLocation)

    template_values = {'CheckLogs': CheckLogs, 'FetchLocation': FetchLocation, 'PageTitle':PageTitle, 'ParentRun':ParentRun}
    self.response.out.write(render_view.full_view('', template_values, 'check_logs_body.html'))
  post = get
  
# DELETE LOGS
class DeleteLogs(webapp.RequestHandler):
  def get(self):
    # Check input key
    InputKey = self.request.get('id')
    if InputKey == 'AuthorizedKeyName':
      # Inititalize Counter - only does 50 per cycle to avoid timeout
      CycleTimer = 0
      # Cycle through all the runs
      CheckRuns = db.GqlQuery("SELECT * "
                              "FROM CheckRun ")	
      if CheckRuns.count() > 0:
        for CheckRun in CheckRuns:
          CheckRun.delete()
          CycleTimer = CycleTimer + 1
          if CycleTimer > 50:
            self.redirect('/admin/checkruns?id=AuthorizedKeyName')
      # Cycle through all the logs
      CheckLogs = db.GqlQuery("SELECT * "
                              "FROM CheckLog ")	
      if CheckLogs.count() > 0:
        for CheckLog in CheckLogs:
          CheckLog.delete()
          CycleTimer = CycleTimer + 1
          if CycleTimer > 50:
            self.redirect('/admin/checkruns?id=AuthorizedKeyName')
    else:
      self.response.out.write('You are not authorized to clear logs')
    self.redirect('/admin/checkruns')
    
  post = get
