from BaseHandler import BaseHandler
from lib.db.User import User

class Login(BaseHandler):
    def get(self):
        self.next_url = self.request.headers.get('referer', '/')
        self.render('login-form.html', next_url = self.next_url)

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        self.next_url = str(self.request.get('next_url'))
        if not self.next_url or self.next_url.startswith('/login'):
            self.next_url = '/'

        u = User.login(username, password)
        if u:
            self.login(u)
            self.done()
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

    def done(self, *a, **kw):
        raise NotImplementedError

class WikiLogin(Login):
    def done(self):
        self.redirect('/wiki' + self.next_url)
