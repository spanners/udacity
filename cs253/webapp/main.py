import os

from webapp2 import WSGIApplication, Route
from webapp2_extras import routes

from Rot13 import Rot13

from Ascii import Ascii

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

        Route(r'/', handler='handlers.HomePage.HomePage', name='home'),

        ('/rot13/?', Rot13),

        ('/ascii/?', Ascii),

        routes.PathPrefixRoute('/blog', [

            Route(r'/',
                handler='handlers.blog.BlogFront.BlogFront',
                name='front',
                ),

            Route(r'/<post_id:[0-9]+>',
                handler='handlers.blog.PostPage.PostPage',
                name='page',
                handler_method='get'),

            Route(r'/newpost',
                handler='handlers.blog.NewPost.NewPost',
                name='newpost'),

            Route(r'/signup',
                handler='handlers.blog.BlogSignup.BlogSignup',
                name='signup'),

            Route(r'/login',
                handler='handlers.blog.BlogLogin.BlogLogin',
                name='login'),

            Route(r'/logout',
                handler='handlers.blog.BlogLogout.BlogLogout',
                name='logout'),

            Route(r'/welcome',
                handler='handlers.blog.Welcome.Welcome',
                name='welcome'),

        ]),

       ('/blog/flush', Flush),

       ('/wiki/signup', WikiSignup),
       ('/wiki/login', WikiLogin),
       ('/wiki/logout', WikiLogout),
       ('/wiki/_edit' + PAGE_RE, WikiEditPage),
       ('/wiki/_history' + PAGE_RE, WikiHistoryPage),
       ('/wiki' + PAGE_RE + '(?:.json)?', WikiPage),

       ],
  debug = DEBUG)
