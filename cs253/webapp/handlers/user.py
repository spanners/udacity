import webapp2

from handlers.base import AppHandler
from lib.utils import grey_style, make_secure_val, check_secure_val
from lib.db.User import User

class UserHandler(AppHandler):
    """ User handler, encapsulating user functions. """

    def __init__(self, request=None, response=None):
        super(UserHandler, self).__init__(request, response)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
        self.jinja.globals['grey_style'] = grey_style

        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'

    def render_str(self, template_name, **params):
        """ Override with params for template to access. """
        template = self.jinja.get_template(template_name)
        params['user'] = self.user
        return template.render(**params)

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def notfound(self):
        self.error(404)
        self.write("<h1>404: Not Found</h1>Sorry, my friend, but that page does not exist.")
