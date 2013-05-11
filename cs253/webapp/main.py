import webapp2

from MainPage import MainPage

DEBUG = False

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([
                               ('/', MainPage),
                               ],
                              debug = DEBUG)
