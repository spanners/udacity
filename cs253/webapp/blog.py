import webapp2

from Signup import BlogSignup
from Welcome import Welcome
from BlogFront import BlogFront
from PostPage import PostPage
from NewPost import NewPost
from Login import BlogLogin
from Logout import BlogLogout
from Flush import Flush

DEBUG = False

app = webapp2.WSGIApplication([
                               ('/blog/?(?:.json)?', BlogFront),
                               ('/blog/([0-9]+)(?:.json)?', PostPage),
                               ('/blog/flush', Flush),
                               ('/blog/newpost', NewPost),
                               ('/blog/signup', BlogSignup),
                               ('/blog/login', BlogLogin),
                               ('/blog/logout', BlogLogout),
                               ('/blog/welcome', Welcome),
                               ],
                              debug=DEBUG)
