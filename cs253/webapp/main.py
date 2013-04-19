import webapp2

from Rot13 import Rot13
from Signup import Register
from Welcome import Welcome
from BlogFront import BlogFront
from PostPage import PostPage
from NewPost import NewPost
from Login import Login
from Logout import Logout
from Ascii import Ascii
from Flush import Flush
from MainPage import MainPage

DEBUG = False

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/rot13/?', Rot13),
                               ('/blog/?(?:.json)?', BlogFront),
                               ('/blog/([0-9]+)(?:.json)?', PostPage),
                               ('/blog/flush', Flush),
                               ('/blog/newpost', NewPost),
                               ('/blog/signup', Register),
                               ('/blog/login', Login),
                               ('/blog/logout', Logout),
                               ('/blog/welcome', Welcome),
                               ('/ascii/?', Ascii),
                               ],
                              debug=True)