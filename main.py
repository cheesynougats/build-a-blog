import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db
import re

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Posts(db.Model):
    subject = db.StringProperty(required = True)
    content = db.StringProperty(required = True)
    created_date = db.DateTimeProperty(auto_now_add = True)

class Redir(webapp2.RequestHandler):

    def get(self):
        self.redirect("/blog")

class Index(webapp2.RequestHandler):

    def get(self):
        posts = db.GqlQuery("SELECT * FROM Posts ORDER BY created_date DESC LIMIT 5")
        t = jinja_env.get_template("frontpage.html")
        content = t.render(posts = posts, error = self.request.get("error"))
        self.response.write(content)

class NewPostHandler(webapp2.RequestHandler):

    def post(self):
        if self.request.get("subject"):
            new_subject = self.request.get("subject")
        else:
            new_subject = ""
        if self.request.get("content"):
            new_content = self.request.get("content")
        else:
            new_content = ""
        t = jinja_env.get_template("newpost.html")
        content = t.render(subject = new_subject, content = new_content, error = self.request.get("error"))
        self.response.write(content)




app = webapp2.WSGIApplication([
    ('/', Redir),
    ('/blog', Index),
    ('/newpost', NewPostHandler)

], debug=True)
