from BaseHandler import BaseHandler

class MainPage(BaseHandler):
  def get(self):
      self.render('main.html')