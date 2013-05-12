import os

from webapp2 import WSGIApplication, Route

from MainPage import MainPage

from Rot13 import Rot13

from Ascii import Ascii

from Signup import BlogSignup
from Welcome import Welcome
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

# Set useful fields
root_dir = os.path.dirname(__file__)
template_dir = os.path.join(root_dir, 'templates')
DEBUG = False
PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = WSGIApplication([
                               ('/', MainPage),

                               ('/rot13/?', Rot13),

                               ('/ascii/?', Ascii),


    Route(r'/blog', handler='handlers.BlogFront.BlogFront', name='front'),
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
