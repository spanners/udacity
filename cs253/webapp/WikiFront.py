from BaseHandler import BaseHandler
#from lib.db.Post import get_posts, age_str

class WikiFront(BaseHandler):
    def get(self):
    	self.render('wikifront.html')
        # posts, age = get_posts()
        # if self.format == 'html':
        #     self.render('wikifront.html', posts = posts, age = age_str(age))
        # else:
        #     return self.render_json([p.as_dict() for p in posts])
