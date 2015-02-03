import webapp2

form = """
    <form method="post">
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

    def post(self):

        q = self.request.get('q')
        
        self.redirect("/thanks", q)


class ThanksHandler(webapp2.RequestHandler):

    def get(self):

        self.response.out.write('you entered: ' + q)


# URLs
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler)
], debug=True)
