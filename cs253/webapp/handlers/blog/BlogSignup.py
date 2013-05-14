from handlers.Signup import UserSignup

class BlogSignup(UserSignup):
    def signin(self):
        self.redirect_to('welcome')
