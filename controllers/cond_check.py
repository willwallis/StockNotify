#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp
from google.appengine.api import users

# Import modules used by this controller
from models.models import *
from controllers import render_view
from controllers import cond_checkjob

# CHECK CONDITIONS AND DISPLAY RESULTS
class CheckCondition(webapp.RequestHandler):
  def get(self):
  # Get prices for current conditions
    PriceSet = cond_checkjob.get_price()
    if PriceSet['Status'] == 'NoRecords':
      Results = {1:{'stock':'','condition':'','price':'','currentprice':'','currentcond':'','match':''}}
    else:
  # Query for Conditions
      QueryUser = users.get_current_user()
      Conditions = db.GqlQuery("SELECT * "
                            "FROM Condition "
                            "WHERE status = :1 "
                            "AND author = :2 "
                            "ORDER BY date DESC ",
                            "Active", QueryUser)
  # Set counter to zero and create blank result set.
      ResultCounter = 0							
      Results = {1:{'stock':'a','condition':'b','price':'c','currentprice':'d','currentcond':'e','match':'f'}}
#      Results.update = {2:{'stock':'ab','condition':'b','price':'c','currentprice':'d','currentcond':'e','match':'f'}}
  # Check whether conditions are met and update status
      for Condition in Conditions:
        ResultCounter = ResultCounter + 1
        current_price = float(PriceSet[Condition.stock])
        cond_price = float(Condition.price)
        current_cond = cond_checkjob.price_compare(current_price, cond_price)
        if current_cond == Condition.expcheck:
          match_cond = 'True'
#        Condition.status = 'Matched'
          Condition.put()
        else:
          match_cond = 'False'	  
        Results.update({ResultCounter:{'stock':Condition.stock,'condition':Condition.expcheck,'price':cond_price,'currentprice':current_price,'currentcond':current_cond,'match':match_cond}})
    template_values = {'results': Results}
    self.response.out.write(render_view.full_view('Check', template_values, 'check_cond_body.html'))
