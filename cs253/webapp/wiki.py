import webapp2

from Signup import WikiSignup
from Login import WikiLogin
from Logout import WikiLogout
from WikiPage import WikiPage
from WikiEditPage import WikiEditPage
from WikiHistoryPage import WikiHistoryPage

DEBUG = False

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([
                               ('/wiki/signup', WikiSignup),
                               ('/wiki/login', WikiLogin),
                               ('/wiki/logout', WikiLogout),                               
                               ('/wiki/_edit' + PAGE_RE, WikiEditPage),
                               ('/wiki/_history' + PAGE_RE, WikiHistoryPage),
                               ('/wiki' + PAGE_RE + '(?:.json)?', WikiPage),
                               ],
                               debug = DEBUG)
