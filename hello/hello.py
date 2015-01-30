import webapp2


form = """
    <form method="post">
        What is your birthday?
        <br>

        <label>Month
            <input type="text" name="month">
        </label>

        <label>Day
            <input type="text" name="day">
        </label>

        <label>Year
            <input type="text" name="year">
        </label>

        <br>
        <br>
        <input type="submit">
    </form>
"""

# form = """
#    <form action="/testform" method="post">
#        <input name="q">
#        <input type="submit">
#    </form>
# """


class MainPage(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(form)

    def post(self):
        self.response.write("Thanks! That's a totally valid day!")

# class TestHandler(webapp2.RequestHandler):
#    def post(self):
#        q = self.request.get('q')
#        self.response.write(q)

        # To see the request headers, comment the above
        # and uncomment the code below.
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write(self.request)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    # ('/testform', TestHandler)
], debug=True)
