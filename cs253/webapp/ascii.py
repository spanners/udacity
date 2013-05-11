import webapp2

from Ascii import Ascii

DEBUG = False

app = webapp2.WSGIApplication([
                               ('/ascii/?', Ascii),
                               ],
                              debug = DEBUG)
