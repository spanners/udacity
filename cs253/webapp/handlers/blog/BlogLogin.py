from handlers.Login import Login

class BlogLogin(Login):
    def done(self):
        self.redirect_to('welcome')
