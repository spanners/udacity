#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

form="""
<form method="post">
    What is your birthday?
    <br>
    <label>Day <input   value="%(day)s"   type="text" name="day"></label>
    <label>Month <input value="%(month)s" type="text" name="month"></label>
    <label>Year <input  value="%(year)s"  type="text" name="year"></label>
    <div style="color:    red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

def valid_month(month):
    months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

    if month.capitalize() in months:
        return month.capitalize()
    else:
        return None

def valid_day(day):
    days = [str(x) for x in range(1,32)]
    if day in days:
        return int(day)
    else:
        return None

def valid_year(year):
    if year.isdigit():
        year_digit = int(year)
        if 1900 <= year_digit <= 2020:
            return year_digit
    return None

def escape_html(s):
    s = s.replace (">", "&gt;")
    s = s.replace ("<", "&lt;")
    s = s.replace ('"', "&quot;")
    s = s.replace ("&", "&amp;")
    return s

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", day="", month="", year=""):
        self.response.out.write(form % {"error": error,
                                        "day"  : escape_html(day),
                                        "month": escape_html(month),
                                        "year" : escape_html(year)})

    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day   = self.request.get('day')
        user_year  = self.request.get('year')

        day   = valid_day(user_day)
        month = valid_month(user_month)
        year  = valid_year(user_year)

        if not (day and month and year):
            self.write_form("That doesn't look valid to me, friend.", user_day,
                    user_month, user_year)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")


app = webapp2.WSGIApplication([('/', MainHandler), ('/thanks', ThanksHandler)],
                              debug=True)