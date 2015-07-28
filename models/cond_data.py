#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp
from google.appengine.api import users

# Import modules used by this controller
from models import *

# WRITES NEW OR UPDATED RECORD TO DATABASE
class Write(webapp.RequestHandler):
  def post(self):
  # Determines if stock exists and gets code if name is chosen
    USStocks = db.GqlQuery("SELECT * "
                            "FROM USStockList "
							"WHERE comboname = :1 ", 
							self.request.get('stock') )
    counter = 0
    StockSymbol = ''
    for Stock in USStocks:
      StockSymbol = Stock.symbol
      counter = counter + 1
    if counter == 0:
      USStocks = db.GqlQuery("SELECT * "
                            "FROM USStockList "
							"WHERE symbol = :1 ", 
							self.request.get('stock') )
    for Stock in USStocks:
      StockSymbol = Stock.symbol
      counter = counter + 1						
    if counter == 0 and len(self.request.get('id')) > 0:
      editstring = '/editcond?id=%s' % (self.request.get('id'))
      self.redirect(editstring)	  
    elif counter == 0:
      self.redirect('/createcond')
    else:
  # Checks to see if edit or new record
      if len(self.request.get('id')) > 0:
        condition = Condition.get(self.request.get('id'))
      else:
        condition = Condition()
  # Writes author of request
      if users.get_current_user():
        condition.author = users.get_current_user()
  # If a new record defaults to Active otherwise sets to user value  
      if len(self.request.get('status')) > 0:
        condition.status = self.request.get('status')
      else:
        condition.status = 'Active'
  # Updates other values, writes record and redirects to main page
      condition.stock = StockSymbol
      condition.price = float(self.request.get('price'))
      condition.expcheck = self.request.get('expcheck')
      if self.request.get('email') == 'true':
        condition.email = True
      else:
        condition.email = False	
      if self.request.get('sms') == 'true':
        condition.sms = True
      else:
        condition.sms = False	
      if self.request.get('phone') == 'true':
        condition.phone = True
      else:
        condition.phone = False	
      condition.put()
      self.redirect('/')
      
# DELETE CONDITION RECORD
class Delete(webapp.RequestHandler):
  def post(self):
  # Checks to see if edit or new record
    if len(self.request.get('id')) > 0:
      condition = Condition.get(self.request.get('id'))
      condition.delete()
    self.redirect('/')
