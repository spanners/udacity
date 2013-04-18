import webapp2
from Post import flush_cache

class Flush(webapp2.RequestHandler):
    def get(self):
        flush_cache()
        self.redirect('/blog')