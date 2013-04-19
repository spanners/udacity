from BaseHandler import BaseHandler
from lib.db.User import User

class Login(BaseHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.done()
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

    def done(self, *a, **kw):
        raise NotImplementedError

class BlogLogin(Login):
    def done(self):
        self.redirect('/blog/welcome')

class WikiLogin(Login):
    def done(self):
        self.redirect('/wiki')