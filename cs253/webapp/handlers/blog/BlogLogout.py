from handlers.Logout import Logout

class BlogLogout(Logout):
    def done(self):
        self.redirect_to('signup')
