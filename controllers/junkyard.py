#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp

# Import modules used by this controller
from controllers import render_view

# Returns a list of US stocks for autocomplete
# Removed for performance reasons. 
def stock_list():
      USStocks = db.GqlQuery("SELECT * "
                            "FROM USStockList ")
      str_list = []
      str_list.append('[') 
      for record in USStocks:
        str_list.append('"') 
        str_list.append(record.comboname)
        str_list.append('",') 
      str_list = str_list[:-1]   
      str_list.append('"]') 
      return ''.join(str_list)
      
      
# CLASS TO DO TESTING WITH
# Used to test concatenating stocks into a string. Replaced with function.
class TestStocks(webapp.RequestHandler):
  def get(self):
      USStocks = db.GqlQuery("SELECT * "
                            "FROM USStockList ")
      str_list = []
      for record in USStocks:
        str_list.append('"') 
        str_list.append(record.comboname)
        str_list.append('",') 
      str_list = str_list[:-1]   
      FinalString  = ''.join(str_list)
      self.response.out.write(FinalString) 