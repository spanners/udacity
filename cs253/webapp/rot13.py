import webapp2

from Rot13 import Rot13

DEBUG = False

app = webapp2.WSGIApplication([
                               ('/rot13/?', Rot13),
                               ],
                              debug = DEBUG)
