import webapp2


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)


class MainPage(Handler):
    # These cookies are not hashed and can be manipuated
    # in the browser console. The purpose of this exercise is
    # to see how cookies work.

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        # store the number of visits in a var
        visits = 0
        visit_cookie_str = self.request.cookies.get('visits')

        # if a cookie exists, then a var, then convert
        # the visits(str) to visits(int)
        if visit_cookie_str:
            visits = int(visit_cookie_str)

        visits += 1
        new_cookie_val = str(visits)

        # write the cookie to store the number of visits
        self.response.headers.add_header('Set-Cookie',
                                         'visits=%s' % new_cookie_val)

        # use the cookie
        if visits > 9 and visits < 100:
            self.write("You have visited the site more "
                       "than %s times!" % visits)
        elif visits >= 100:
            self.write("Wow! You have visited the site more "
                       "than %s times!" % visits)
        else:
            # write the amount of visits to the page
            self.write("You've been here %s times." % visits)


application = webapp2.WSGIApplication([('/visits', MainPage)], debug=True)
