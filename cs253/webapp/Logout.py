from BaseHandler import BaseHandler

class Logout(BaseHandler):
    def get(self):
    	self.next_url = self.request.headers.get('referer', '/')

        self.logout()
        self.done()

    def done(self, *a, **kw):
    	raise NotImplementedError

class BlogLogout(Logout):
	def done(self):
		self.redirect('/blog/signup')

class WikiLogout(Logout):
	def done(self):
		self.redirect(self.next_url)