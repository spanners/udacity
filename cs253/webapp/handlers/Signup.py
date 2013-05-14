from handlers.user import UserHandler

from lib.utils import valid_username, valid_password, valid_email
from lib.db.User import User

class Signup(UserHandler):
    def get(self):
        self.next_url = self.request.headers.get('referer', '/')
        self.render("signup-form.html", next_url = self.next_url)

    def post(self):
        have_error = False

        self.next_url = str(self.request.get('next_url'))
        if not self.next_url or self.next_url.startswith('/login'):
            self.next_url = '/'

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

class UserSignup(Signup):
    def done(self):
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists'
            self.redner('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.signin()

    def signin(self, *a, **kw):
        raise NotImplementedError

class WikiSignup(UserSignup):
    def signin(self):
        self.redirect('/wiki' + self.next_url)
