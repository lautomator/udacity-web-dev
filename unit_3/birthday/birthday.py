import webapp2
import cgi


form = """
    <form method="post">
        What is your birthday?
        <br>

        <label>
            Month
            <input type="text" name="month" value="%(month)s">
        </label>
        <br>

        <label>
            Day
            <input type="text" name="day" value="%(day)s">
        </label>
        <br>

        <label>
            Year
            <input type="text" name="year" value="%(year)s">
        </label>
        <br>

        <div style="color: red">%(error)s</div>

        <br>
        <br>
        <input type="submit">
    </form>
"""


class MainPage(webapp2.RequestHandler):

    def write_form(self, error='', month="", day="", year=""):
        self.response.write(form % {
            'error': error,
            'month': escape_html(month),
            'day': escape_html(day),
            'year': escape_html(year)
        })

    def get(self):

        self.write_form()

    def post(self):

        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (month and day and year):
            self.write_form(
                "That does not look valid.",
                user_month, user_day, user_year)
        else:
            self.redirect("/thanks")


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Thanks! That's a totally valid day!")
z
# class TestHandler(webapp2.RequestHandler):
#    def post(self):
#        q = self.request.get('q')
#        self.response.write(q)
#
# To see the request headers, comment the above
#        and uncomment the code below.
#        self.response.headers['Content-Type'] = 'text/plain'
#        self.response.write(self.request)


# URLs
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler)
    # ('/testform', TestHandler)
], debug=True)


# escape nasty html chars
def escape_html(s):

    return cgi.escape(s, quote=True)


# validation functions below
def valid_month(month):

    months = [
        'January',
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
        'December'
    ]

    # dictionary with the first 3 letters (key) and month (value):
    months_abbv = dict((m[:3].lower(), m) for m in months)

    if month:
        short_month = month[:3].lower()
        return months_abbv.get(short_month)


def valid_day(day):

    # valid day range
    days = range(1, 32)

    for d in days:
        if str(d) == day:
            return int(day)


def valid_year(year):

    if year.isdigit():
        if int(year) >= 1900 and int(year) <= 2020:
            return int(year)
