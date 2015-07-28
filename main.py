# Importing some of Google's AppEngine modules:
import webapp2

# Importing the controllers that will handle the generation of the pages:
from controllers import cond_ctrl, cond_check, cond_checkjob, about, logs, settings, users, message, test
from models import cond_data, stock_loader, twilio_data, user_data
	
# This is the main method that maps the URLs

app = webapp2.WSGIApplication([
#    ('/', users.LoginCheck),
    # Condition pages
    ('/', cond_ctrl.List),   
    ('/condlist', cond_ctrl.List),   
    ('/createcond', cond_ctrl.Create),   
    ('/editcond', cond_ctrl.Edit),   
    ('/savecond', cond_data.Write),   
    ('/deletecond', cond_data.Delete),
    ('/checkcond', cond_check.CheckCondition),
    # Admin pages
    ('/admin/checkruns', logs.CheckRuns),
    ('/admin/checklogs', logs.CheckLogs),
    ('/admin/deletelogs', logs.DeleteLogs),
    ('/admin/checksettings', settings.CheckSettings),
    ('/admin/users', users.Users),   
    ('/myprofile', users.MyProfile),   
    # User Profile
    ('/admin/userprofile', users.UserProfile),
    ('/saveuser', user_data.WriteUser),
    ('/savemyuser', user_data.WriteMyUser),
    ('/deleteuser', user_data.DeleteUser),
    # Twilio
    ('/admin/twiprofile', users.TwiProflie),
    ('/savetwilio', twilio_data.WriteTwilio),
    ('/deletetwilio', twilio_data.DeleteTwilio),
    # Other
    ('/admin/test', test.Test),
    ('/about', about.About),
    # Jobs
    ('/checkjob', cond_checkjob.CheckConditionJob),
    ('/message/match', message.MatchMessage),
    ('/loadstocks', stock_loader.LoadStocks)      
], debug=True)
