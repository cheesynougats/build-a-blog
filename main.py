import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db
import re

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Redir(webapp2.RequestHandler):

    def get(self):
        self.redirect("/blog")

class Index(webapp2.RequestHandler):

    def get(self):
        self.response.write("Post Index")

class NewPostHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write("New Post")




app = webapp2.WSGIApplication([
    ('/', Redir),
    ('/blog', Index),
    ('/newpost', NewPostHandler)

], debug=True)
