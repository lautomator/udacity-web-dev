import os
import re
import random
import hashlib
import hmac
import string
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

secret = 'nvSqlliCsiKCcfdsYAiTtvqbqwtDJxLSWxLgLfpZlZpKgApJMs'

# regexs for validation:
_user_re = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
_pw_re = re.compile(r'^.{3,20}$')
_email_re = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def make_secure_val(s):
    return "%s|%s" % (s, hmac.new(secret, s).hexdigest())


def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val


# validation procedures
def valid_username(s):
    return _user_re.match(s)


def valid_password(s1):
    return _pw_re.match(s1)


def valid_verify(s1, s2):
    return s1 == s2


def valid_email(s):
    return _email_re.match(s)


class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    # login and logout functions will go here

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


def make_salt(length=5):
    return ''.join(random.choice(string.letters) for x in range(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        s = make_salt()
    h = hashlib.sha256(name + pw + s).hexdigest()
    return '%s,%s' % (h, s)


def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)


def users_key(group='default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()  # optional

    # decorators
    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name=', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


class Signup(BlogHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        have_error = False
        self.user_username = self.request.get('username')
        self.user_password = self.request.get('password')
        self.user_verify = self.request.get('verify')
        self.user_email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['err_name'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['err_password'] = "That's not a valid password."
            have_error = True

        elif self.password != self.verify:
            params['err_verify'] = "Passwords do not match."

        if not valid_email(self.email):
            params['err_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('login.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class DoneSignup(Signup):
    def done(self):
        self.redirect('/welcome/welcome?username=' + self.username)


class Register(Signup):
    def done(self):
        # verify the user does not already exist
        u = User.by_name(self.username)
        if u:
            msg = 'User already exists'
            self.render('login.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/welcome')


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome, ")

# URL mapping
application = webapp2.WSGIApplication([
    ('/signup', Register),
    ('/welcome', WelcomeHandler)
], debug=True)
