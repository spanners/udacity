from BaseHandler import BaseHandler
from lib.db.Post import get_posts, age_str

class BlogFront(BaseHandler):
    def get(self):
        posts, age = get_posts()
        if self.format == 'html':
            self.render('blogfront.html', posts = posts, age = age_str(age))
        else:
            return self.render_json([p.as_dict() for p in posts])
