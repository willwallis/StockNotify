#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp
import os
import csv

# Import modules used by this controller
from models import *

# CLASS TO LOAD LIST OF US STOCKS
class LoadStocks(webapp.RequestHandler):
  def get(self):
    inputid = self.request.get('action')
    if inputid == 'Load':
      inputfile = os.path.join(os.path.dirname(__file__), '../data' ,self.request.get('file'))
      reader = csv.reader(open(inputfile, 'rb'), delimiter=',', quotechar='"')
      counter = 0
      for row in reader:
        stockrecord = USStockList()
        stockrecord.exchange = row[0]
        stockrecord.symbol = row[1]
        stockrecord.name = row[2]
        stockrecord.comboname = row[3]
        stockrecord.put()
        counter = counter + 1		
      self.response.out.write('%s records added' % (str(counter)))
    elif inputid == 'Delete':
      USStocks = db.GqlQuery("SELECT * "
                            "FROM USStockList ")
      counter = 0
      for record in USStocks:
        record.delete()
        counter = counter + 1		
      self.response.out.write('%s records deleted' % (str(counter)))
    elif inputid == 'Count':
      USStocks = db.GqlQuery("SELECT * "
                            "FROM USStockList ")
      counter = USStocks.count(limit=10000)
      self.response.out.write('%s records' % (str(counter)))
    else:
      self.response.out.write('Please add an ?Action of Load or Delete')	  