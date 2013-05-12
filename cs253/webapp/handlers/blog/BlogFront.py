from handlers.user import UserHandler
from lib.db.Post import get_posts, age_str

class BlogFront(UserHandler):
    def get(self, garbage):
        posts, age = get_posts()
        if self.format == 'html':
            self.render('blogfront.html', posts = posts, age = age_str(age))
        elif self.format == 'json':
            return self.render_json([p.as_dict() for p in posts])
