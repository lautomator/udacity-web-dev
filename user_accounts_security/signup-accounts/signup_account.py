import os
import re
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)


# regexs for validation:
_user_re = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
_pw_re = re.compile(r'^.{3,20}$')
_email_re = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


# validation procedures
def valid_username(s):
    return _user_re.match(s)


def valid_password(s1):
    return _pw_re.match(s1)


def valid_verify(s1, s2):
    return s1 == s2


def valid_email(s):
    return _email_re.match(s)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):

    def get(self):

        self.render(
            "login.html",
            err_name='',
            err_password='',
            err_verify='',
            err_email='',
            username='',
            password='',
            verify='',
            email='')

    def post(self):

        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')

        username = valid_username(user_username)
        password = valid_password(user_password)
        verify = valid_verify(user_password, user_verify)
        email = valid_email(user_email)  # email is an optional field
        email_ok = True

        # validate the fields and store errors
        # populates the empty list with placeholder values
        err = [s for s in (' ' * 8)]

        if not username:
            err[0] = "That's not a valid username."

        if not password:
            err[1] = "That's not a valid password."

        if not verify:
            err[2] = "Passwords do not match."

        if user_email and not email:
            err[3] = "That's not a valid email."
            email_ok = False

        if (username and password and verify and email_ok):

            self.redirect('/welcome')

        else:
            self.render(
                "login.html",
                err_name=err[0],
                err_password=err[1],
                err_verify=err[2],
                err_email=err[3],
                username=user_username,
                password='',
                verify='',
                email='')


class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.cookies.get('username')

        self.response.headers.add_header(
            'Set-Cookie',
            'username=%s' % username)

        # username = self.request.get(username_cookie)

        self.response.out.write("Welcome, " + username)

# URL mapping
application = webapp2.WSGIApplication([
    ('/signup', MainPage),
    ('/welcome', WelcomeHandler)
], debug=True)
