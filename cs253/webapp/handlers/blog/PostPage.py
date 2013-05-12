from handlers.user import UserHandler
from lib.db.Post import age_get, age_set, age_str, blog_key

from google.appengine.ext import db

class PostPage(UserHandler):
    def get(self, post_id):
        post_key = 'POST_' + post_id

        post, age = age_get(post_key)
        if not post:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key)
            post = db.get(key)
            age_set(post_key, post)
            age = 0

        if not post:
            self.error(404)
            return

        if self.format == 'html':
            self.render("permalink.html", post = post, age = age_str(age))
        elif self.format == 'json':
            self.render_json(post.as_dict())
