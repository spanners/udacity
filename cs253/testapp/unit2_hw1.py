import rot13
import webapp2

form="""
<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(rot13)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""

def escape_html(s):
    s = s.replace (">", "&gt;")
    s = s.replace ("<", "&lt;")
    s = s.replace ('"', "&quot;")
    s = s.replace ("&", "&amp;")
    return s

class MainHandler(webapp2.RequestHandler):
    def write_form(self, text=""):
        self.response.out.write(form % {"rot13": escape_html(text)})

    def get(self):
        self.write_form()

    def post(self):
        text = self.request.get('text')
        rot13_text = rot13.rot13(text)

        self.write_form(rot13_text)

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)