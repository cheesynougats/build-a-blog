import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db
import re

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Blog_post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.StringProperty(required = True)
    created_date = db.DateTimeProperty(auto_now_add = True)

class Redir(webapp2.RequestHandler):

    def get(self):
        self.redirect("/blog")

class Index(webapp2.RequestHandler):

    def get(self):
        posts = db.GqlQuery("SELECT * FROM Blog_post ORDER BY created_date DESC LIMIT 5")
        t = jinja_env.get_template("frontpage.html")
        content = t.render(posts = posts, error = self.request.get("error"))
        self.response.write(content)

class NewPostHandler(webapp2.RequestHandler):

    def get(self):
        if self.request.get("subject"):
            new_subject = self.request.get("subject")
        else:
            new_subject = ""
        t = jinja_env.get_template("newpost.html")
        content = t.render(subject = new_subject, error = self.request.get("error"))
        self.response.write(content)

    def post(self):
        subject_entered = self.request.get("subject") and (self.request.get("subject").strip() != "")
        content_entered = self.request.get("content") and (self.request.get("content").strip() != "")
        if subject_entered and content_entered:
            new_subject = cgi.escape(self.request.get("subject"), quote = True)
            new_content = cgi.escape(self.request.get("content"), quote = True)
            post = Blog_post(subject = new_subject, content = new_content)
            post.put()
            self.redirect("/blog")
        else:
            error = "Please enter a subject and blog post content."
            subject = cgi.escape(self.request.get("subject"), quote = True)
            self.redirect("/newpost?error=" + error + "&subject=" + subject)





app = webapp2.WSGIApplication([
    ('/', Redir),
    ('/blog', Index),
    ('/newpost', NewPostHandler)

], debug=True)
