from handlers.user import UserHandler

class Logout(UserHandler):
    def get(self):
    	self.next_url = self.request.headers.get('referer', '/')

        self.logout()
        self.done()

    def done(self, *a, **kw):
    	raise NotImplementedError

class WikiLogout(Logout):
	def done(self):
		self.redirect(self.next_url)
