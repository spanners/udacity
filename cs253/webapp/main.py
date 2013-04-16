import json

import webapp2

from util import *
from models import *

from google.appengine.ext import db

DEBUG = True

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return j_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'

class MainPage(BlogHandler):
  def get(self):
      self.render('main.html')

class BlogFront(BlogHandler):
    def get(self):
        posts, age = get_posts()
        if self.format == 'html':
            self.render('front.html', posts = posts, age = age_str(age))
        else:
            return self.render_json([p.as_dict() for p in posts])

class PostPage(BlogHandler):
    def get(self, post_id):
        post_key = 'POST_' + post_id

        post, age = age_get(post_key)
        if not post:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key)
            post = db.get(key)
            age_set(post_key, post)
            age = 0

        if not post:
            self.error(404)
            return

        if self.format == 'html':
            self.render("permalink.html", post = post, age = age_str(age))
        elif self.format == 'json':
            self.render_json(post.as_dict())

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/blog/login")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key, subject = subject, content = content)
            post_id = add_post(p)
            self.redirect('/blog/%s' % post_id)
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)

class Rot13(BlogHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html', text = rot13)


class Signup(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Unit2Signup(Signup):
    def done(self):
        self.redirect('/unit2/welcome?username=' + self.username)

class Register(Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog/welcome')

class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog/welcome')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog/signup')

class Unit3Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/blog/signup')

class Welcome(BlogHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')

class Flush(webapp2.RequestHandler):
    def get(self):
        flush_cache()
        self.redirect('/blog')

class Ascii(BlogHandler):
    def render_front(self, title="", art="", error=""):
        arts = top_arts()

        img_url = None
        points = filter(None, (a.coords for a in arts))
        if points:
            img_url = gmap_img(points)

        #display the image URL
        self.render("ascii.html", title = title, art = art, error = error, arts = arts, img_url = img_url)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            p = Art(parent=art_key, title = title, art = art)
            #lookup the user's coordinates from their IP
            coords = get_coords(self.request.remote_addr)
            #if we have coordinates, add them to the art
            if coords:
                    p.coords = coords
            p.put()
            #rerun the query and update the cache
            top_arts(True)

            self.redirect("/ascii")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(error = error, title = title, art =art)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/rot13/?', Rot13),
                               ('/unit2/signup', Unit2Signup),
                               ('/unit2/welcome', Welcome),
                               ('/blog/?(?:.json)?', BlogFront),
                               ('/blog/([0-9]+)(?:.json)?', PostPage),
                               ('/blog/flush', Flush),
                               ('/blog/newpost', NewPost),
                               ('/blog/signup', Register),
                               ('/blog/login', Login),
                               ('/blog/logout', Logout),
                               ('/blog/welcome', Unit3Welcome),
                               ('/ascii/?', Ascii)
                               ],
                              debug=True)
