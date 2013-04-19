import webapp2

from Rot13 import Rot13

from Signup import BlogSignup, WikiSignup
from Welcome import Welcome
from BlogFront import BlogFront
from PostPage import PostPage
from NewPost import NewPost
from Login import BlogLogin, WikiLogin
from Logout import BlogLogout, WikiLogout
from Ascii import Ascii
from Flush import Flush

from MainPage import MainPage

from WikiFront import WikiFront

DEBUG = False

app = webapp2.WSGIApplication([('/', MainPage),

                               ('/wiki', WikiFront),
                               ('/wiki/logout', WikiLogout),
                               ('/wiki/login', WikiLogin),
                               ('/wiki/signup', WikiSignup),

                               ('/rot13/?', Rot13),
                               ('/blog/?(?:.json)?', BlogFront),
                               ('/blog/([0-9]+)(?:.json)?', PostPage),
                               ('/blog/flush', Flush),
                               ('/blog/newpost', NewPost),
                               ('/blog/signup', BlogSignup),
                               ('/blog/login', BlogLogin),
                               ('/blog/logout', BlogLogout),
                               ('/blog/welcome', Welcome),
                               ('/ascii/?', Ascii),
                               ],
                              debug=True)