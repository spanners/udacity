import webapp2
from lib.db.Post import flush_cache

class Flush(webapp2.RequestHandler):
    def get(self):
        flush_cache()
        self.redirect('/blog')