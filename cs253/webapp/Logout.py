from BaseHandler import BaseHandler

class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/blog/signup')