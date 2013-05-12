import webapp2

from MainPage import MainPage

from Rot13 import Rot13

from Ascii import Ascii

from Signup import BlogSignup
from Welcome import Welcome
from BlogFront import BlogFront
from PostPage import PostPage
from NewPost import NewPost
from Login import BlogLogin
from Logout import BlogLogout
from Flush import Flush

from Signup import WikiSignup
from Login import WikiLogin
from Logout import WikiLogout
from WikiPage import WikiPage
from WikiEditPage import WikiEditPage
from WikiHistoryPage import WikiHistoryPage

DEBUG = False

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([
                               ('/', MainPage),

                               ('/rot13/?', Rot13),

                               ('/ascii/?', Ascii),

                               ('/blog/?(?:.json)?', BlogFront),
                               ('/blog/([0-9]+)(?:.json)?', PostPage),
                               ('/blog/flush', Flush),
                               ('/blog/newpost', NewPost),
                               ('/blog/signup', BlogSignup),
                               ('/blog/login', BlogLogin),
                               ('/blog/logout', BlogLogout),
                               ('/blog/welcome', Welcome),

                               ('/wiki/signup', WikiSignup),
                               ('/wiki/login', WikiLogin),
                               ('/wiki/logout', WikiLogout),
                               ('/wiki/_edit' + PAGE_RE, WikiEditPage),
                               ('/wiki/_history' + PAGE_RE, WikiHistoryPage),
                               ('/wiki' + PAGE_RE + '(?:.json)?', WikiPage),

                               ],
                              debug = DEBUG)
