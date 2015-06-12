import webapp2
import hmac

SECRET = 'imsosecret'


def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()


def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)


class MainPage(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        # store the number of visits in a var
        visits = 0
        visit_cookie_str = self.request.cookies.get('visits')

        if visit_cookie_str:
            cookie_val = check_secure_val(visit_cookie_str)
            if cookie_val:
                visits = int(cookie_val)

        visits += 1

        new_cookie_val = make_secure_val(str(visits))

        # write the cookie to store the number of visits
        self.response.headers.add_header('Set-Cookie',
                                         'visits=%s' % new_cookie_val)

        # use the cookie
        if visits > 9:
            self.write("You have visited the site more "
                       "than %s times!" % visits)
        else:
            # write the amount of visits to the page
            self.write("You've been here %s times." % visits)


application = webapp2.WSGIApplication([('/', MainPage)], debug=True)
