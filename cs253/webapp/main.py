import os

from webapp2 import WSGIApplication, Route
from webapp2_extras import routes

from MainPage import MainPage

from Rot13 import Rot13

from Ascii import Ascii

from Signup import BlogSignup
from Welcome import Welcome
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

        routes.PathPrefixRoute('/blog', [

            Route(r'/<garbage:(?:.json)?>',
                handler='handlers.blog.BlogFront.BlogFront',
                name='front',
                handler_method='get'),

        Route(r'/<post_id:[0-9]+><garbage:(?:.json)?>',
            handler='handlers.blog.PostPage.PostPage',
            name='page',
            handler_method='get'),

        Route(r'/newpost',
            handler='handlers.blog.NewPost.NewPost',
            name='newpost'),
        ]),

       ('/blog/signup', BlogSignup),
       ('/blog/login', BlogLogin),
       ('/blog/logout', BlogLogout),
       ('/blog/welcome', Welcome),
       ('/blog/flush', Flush),

       ('/wiki/signup', WikiSignup),
       ('/wiki/login', WikiLogin),
       ('/wiki/logout', WikiLogout),
       ('/wiki/_edit' + PAGE_RE, WikiEditPage),
       ('/wiki/_history' + PAGE_RE, WikiHistoryPage),
       ('/wiki' + PAGE_RE + '(?:.json)?', WikiPage),

       ],
  debug = DEBUG)
