import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class BaseHandler(webapp2.RequestHandler):
  """ Convenience functions common to many classes. """
  def write(self, *a, **kw):
    """ Inheriting classes need only type self.write(..). """
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))


class Main(BaseHandler):
  def get(self):
    self.render('main.html')

class Unit2(BaseHandler):
  def get(self):
    self.render('unit2.html')

class Unit3(BaseHandler):
  def get(self):
    self.render('unit3.html')

class Rot13(BaseHandler):
  def get(self):
    self.render('rot13-form.html')

  def post(self):
    rot13 = ''
    text = self.request.get('text')
    if text:
      rot13 = text.encode('rot_13')

    self.render('rot13-form.html', text = rot13)

import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

class Signup(BaseHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify   = self.request.get('verify')
        user_email    = self.request.get('email')

        username = valid_username(user_username)
        password = valid_password(user_password)
        verify = None
        if password and user_verify == user_password:
            verify = password
        email = None
        if user_email != "":
            email    = valid_email(user_email)

        username_error = password_error = verify_error = email_error = ""
        is_error = False
        if not username:
            is_error = True
            username_error = "That's not a valid username."
        if not password:
            is_error = True
            password_error = "That wasn't a valid password."
        elif not verify:
            is_error = True
            verify_error = "Your passwords didn't match."
        if user_email != "" and not email:
            is_error = True
            email_error = "That's not a valid email."

        if not is_error:
            self.redirect('/unit2/welcome?username=' + user_username)
        else:
            self.render('signup.html', username = user_username,
                                       email = user_email,
                                       username_error = username_error,
                                       password_error = password_error,
                                       verify_error = verify_error,
                                       email_error = email_error)
class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')

class Ascii(BaseHandler):

  def render_front(self, title="", art="", error=""):
    self.render('ascii.html', title=title, art=art, error=error)

  def get(self):
    self.render_front()

  def post(self):
    title = self.request.get("title")
    art = self.request.get("art")

    if title and art:
      self.write("thanks!")
    else:
      error = "we need both a title and some artwork!"
      self.render_front(title, art, error)

app = webapp2.WSGIApplication([('/', Main),
                               ('/unit2', Unit2),
                               ('/unit3', Unit3),
                               ('/unit2/rot13', Rot13), 
                               ('/unit2/signup', Signup),
                               ('/unit2/welcome', Welcome),
                               ('/unit3/ascii', Ascii)],
                              debug=True)