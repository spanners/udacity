from datetime import datetime, timedelta

from google.appengine.ext import db
from google.appengine.api import memcache

from ..utils import jinja_str

def age_set(key, val):
    save_time = datetime.utcnow()
    memcache.set(key, (val, save_time))

def age_get(key):
    r = memcache.get(key)
    if r:
        val, save_time = r
        age = (datetime.utcnow() - save_time).total_seconds()
    else:
        val, age = None, 0
    return val, age

def add_post(post):
    post.put()
    get_posts(update = True)
    return str(post.key().id())

def get_posts(update = False):
    mc_key = 'BLOGS'

    posts, age = age_get(mc_key)
    if update or posts is None:
        q = db.GqlQuery("SELECT * "
                        "FROM Post "
                        "WHERE ANCESTOR IS :1 "
                        "ORDER BY created DESC "
                        "LIMIT 10",
                        blog_key)
        posts = list(q)
        age_set(mc_key, posts)

    return posts, age

def age_str(age):
    s = 'Queried %s seconds ago'
    age = int(age)
    if age == 1:
        s = s.replace('seconds', 'second')
    return s % age

def flush_cache():
    memcache.flush_all()
    

blog_key = db.Key.from_path('Blogs', 'blogs')

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        return jinja_str("post.html", p = self)

    def as_dict(self):
        time_fmt = '%c'
        d = {'subject': self.subject,
             'content': self.content,
             'created': self.created.strftime(time_fmt),
             'last_modified': self.last_modified.strftime(time_fmt)}
        return d