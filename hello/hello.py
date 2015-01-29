import webapp2


form = """
    <form action="/testform" method="post">
        <input name="q">
        <input type="submit">
    </form>
"""


class MainPage(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(form)


class TestHandler(webapp2.RequestHandler):
    def post(self):
        q = self.request.get('q')
        self.response.write(q)

        # To see the request headers, comment the above
        # and uncomment the code below.
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write(self.request)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/testform', TestHandler)
], debug=True)
