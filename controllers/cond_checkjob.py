#!/usr/bin/env python
# Importing some of Google's AppEngine modules:
from google.appengine.ext import webapp
import urllib
import csv

# Import modules used by this controller
from models.models import *
from controllers import communication

# Requests stock details from Yahoo. Different stats return different details. http://www.gummy-stuff.org/Yahoo-data.htm for codes.
def get_price(): 
  # Get a distinct list of stocks in conditions
    Conditions = db.GqlQuery("SELECT * "
                            "FROM Condition "
                            "WHERE status = :1 "
                            "ORDER BY date DESC LIMIT 50",
                            "Active")	
    PriceSet = {}
    if Conditions.count() > 0:
      DistinctStock = []
      for Condition in Conditions:
        if Condition.stock not in DistinctStock:
          DistinctStock.append(Condition.stock)
      CheckList = ''
      for Stock in DistinctStock:
        CheckList = CheckList + Stock + '+'
      CheckList = CheckList[:-1]
  # Get prices from Yahoo
      stat = 'sl1'
      url = ''.join(('http://finance.yahoo.com/d/quotes.csv?s=',CheckList,'&f=', stat))
      reader = csv.reader(urllib.urlopen(url))
      for row in reader:
        PriceSet[row[0]] = row[1]
    else:
      PriceSet['Status'] = 'NoRecords'
    PriceSet['Status'] = 'Ok'
    return PriceSet

# Compares two prices, current and conditional
def price_compare(current_price, cond_price):	
    if current_price > cond_price:
      return 'Above'
    elif current_price < cond_price:
      return 'Below'	
    elif current_price == cond_price:
      return 'Equal'
      
# A JOB FOR CHECKING CONDITIONS  
class CheckConditionJob(webapp.RequestHandler):
  def get(self):
  # Create record to record run
    checkrun = CheckRun()
    checkrun.put()
    run_key = checkrun.key()
    runcounter = 0
    matchcounter = 0
  # Determine if detailed logs are required
    JobSetting = db.GqlQuery("SELECT * FROM CheckJobSettings ")
    if JobSetting.count() > 0:
      Settings = JobSetting.get()
      DetailLog = Settings.detaillog
    else:
      DetailLog = True
  # Get prices for current conditions
    PriceSet = get_price()
  # Query for Conditions
    Conditions = db.GqlQuery("SELECT * "
                            "FROM Condition "
                            "WHERE status = :1 "
                            "ORDER BY date DESC",
                            "Active")
							
  # Cycle through conditions
    for Condition in Conditions:
      runcounter = runcounter + 1  
      current_price = float(PriceSet[Condition.stock])
      cond_price = float(Condition.price)
      current_cond = price_compare(current_price, cond_price)
      if current_cond == Condition.expcheck:
        match_cond = True
        matchcounter = matchcounter + 1		
        Condition.status = 'Matched'
        Condition.put()
      else:
        match_cond = False	  
  # Write DB record here
      if match_cond == True or DetailLog == True:
        checklog = CheckLog(parent=run_key)
        checklog.stock = Condition.stock
        checklog.condexpcheck = Condition.expcheck
        checklog.email = Condition.email
        checklog.sms = Condition.sms
        checklog.phone = Condition.phone
        checklog.condprice = cond_price
        checklog.currprice = current_price
        checklog.currexpcheck = current_cond
        checklog.currmatch = match_cond
        checklog.requestor = Condition.author
        checklog.condition = str(Condition.key())
        checklog.put()
  # Record check run counters
    checkrun.condcount = runcounter
    checkrun.matchcount = matchcounter
    checkrun.put()	  
  # Send emails for successful matches
    Emaillog = db.GqlQuery("SELECT * "
                            "FROM CheckLog "
                            "WHERE ANCESTOR IS :1 AND email = :2 AND currmatch = :3 "
							"ORDER BY date DESC",
							run_key, True, True)
    for Record in Emaillog:
      message_text = 'The condition for %s has been triggered. The condition was %s %s. The current price is %s, which is %s %s.' % (Record.stock, Record.condexpcheck, Record.condprice, Record.currprice, Record.currexpcheck, Record.condprice)
  #    self.response.out.write(message_text)
      communication.notify_email(Record.requestor, message_text, Record.stock)	  

  # Send SMS for successful matches - TBD
    SMSlog = db.GqlQuery("SELECT * "
                            "FROM CheckLog "
                            "WHERE ANCESTOR IS :1 AND sms = :2 AND currmatch = :3 "
							"ORDER BY date DESC",
							run_key, True, True)
    for Record in SMSlog:
      message_text = 'The condition for %s has been triggered. The condition was %s %s. The current price is %s, which is %s %s. SMS<br />' % (Record.stock, Record.condexpcheck, Record.condprice, Record.currprice, Record.currexpcheck, Record.condprice)
  #    self.response.out.write(message_text)
      communication.notify_sms(Record.requestor, message_text)
  
  # Make phone calls for successful matches - TBD
    Phonelog = db.GqlQuery("SELECT * "
                            "FROM CheckLog "
                            "WHERE ANCESTOR IS :1 AND phone = :2 AND currmatch = :3 "
							"ORDER BY date DESC",
							run_key, True, True)
    for Record in Phonelog:	  
      message_url = 'http://stocknotify.appspot.com/message/match?id=%s' % (Record.key())
  #    self.response.out.write(message_url)
      communication.make_call(Record.requestor, message_url)
