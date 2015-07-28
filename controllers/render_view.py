#!/usr/bin/env python
from google.appengine.api import users
#from google.appengine.ext.webapp import template
import os
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def full_view(highlight, template_values, template_file): 
  # Render Header
    head_template_values = {'Highlight' : highlight, "UserAdmin": users.is_current_user_admin(), 'LogoutURL' : users.create_logout_url("/")}
    headerpath = 'header.html'
    headtemplate = JINJA_ENVIRONMENT.get_template(headerpath)
    header = headtemplate.render(head_template_values)
  # Render Body
    bodypath = template_file
    bodytemplate = JINJA_ENVIRONMENT.get_template(bodypath)
    body = bodytemplate.render(template_values)
  # Render Footer
    foot_template_values = {}
    footerpath = 'footer.html'
    foottemplate = JINJA_ENVIRONMENT.get_template(footerpath)
    footer = foottemplate.render(foot_template_values)
    fullview = header + body + footer
    return fullview