from handlers.user import UserHandler
from lib.db.Post import Post, blog_key, add_post

class NewPost(UserHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect_to('login')

    def post(self):
        if not self.user:
            self.redirect_to('front')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key, subject = subject, content = content)
            post_id = add_post(p)
            self.redirect_to('page', post_id = post_id)
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)
