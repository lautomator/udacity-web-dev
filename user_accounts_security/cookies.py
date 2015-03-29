import webapp2


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)


class MainPage(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        # store the number of visits in a var
        visits = self.request.cookies.get('visits', '0')

        # visits needs to be an integer
        # increment the amount of visits
        if visits.isdigit():
            visits = int(visits) + 1
        else:
            visits = 0

        # write the cookie to store the number of visits
        self.response.headers.add_header('Set-Cookie', 'visits=%s' % visits)

        # use the cookie
        if visits > 9:
            self.write("You have visited the site more"
                       "than %s times!" % visits)
        else:
            # write the amount of visits to the page
            self.write("You've been here %s times." % visits)


application = webapp2.WSGIApplication([('/', MainPage)], debug=True)
