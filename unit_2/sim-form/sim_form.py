import webapp2

form = """
    <form method="post" action="/testform">
        <label>
            Say something:
            <input type="text" name="q">
        </label>

        <br>
        <input type="submit">
    </form>
"""


class MainPage(webapp2.RequestHandler):

    def get(self):

        self.response.out.write(form)


class TestHandler(webapp2.RequestHandler):

    def post(self):
        q = self.request.get('q')
        self.response.out.write('you entered: ' + q + "<br><br>")
        
        # The actual headers
        self.response.out.write(self.request)

# To see the request headers, comment the above
#        and uncomment the code below.
#        self.response.headers['Content-Type'] = 'text/plain'
#        self.response.write(self.request)

# URLs
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/testform', TestHandler)
], debug=True)
