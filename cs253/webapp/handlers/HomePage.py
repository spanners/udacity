from handlers.base import AppHandler

class HomePage(AppHandler):
  def get(self):
      self.render('index.html')
