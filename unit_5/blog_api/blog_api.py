import os
import re
import random
import hashlib
import hmac
from string import letters
import json

import webapp2
import jinja2

from google.appengine.ext import db

# templating directives
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

secret = 'nvSqlliCsiKCcfds'

# global regexs for validation:
_user_re = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
_pw_re = re.compile(r'^.{3,20}$')
_email_re = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


# global validation procedures
def valid_username(s):
    return _user_re.match(s)


def valid_password(s1):
    return _pw_re.match(s1)


def valid_verify(s1, s2):
    return s1 == s2


def valid_email(s):
    return _email_re.match(s)


# security
def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


def make_salt(length=5):
    # return ''.join(random.choice(string.letters) for x in range(length))
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, pw, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, pw, salt)


def users_key(group='default'):
    return db.Key.from_path('users', group)


# blog
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Blog(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):
    def render_front(self, subject="", content="", error=""):
        all_posts = db.GqlQuery("SELECT * FROM Blog "
                                "ORDER BY created DESC")

        # get the 10 most recent
        posts = all_posts[0:10]

        self.render(
            "blog.html",
            subject=subject,
            content=content,
            error=error,
            posts=posts)

    def get(self):
        self.render_front()


class NewPost(Handler):
    def render_post(self, subject="", content="", error=""):

        self.render(
            "newpost.html",
            subject=subject,
            content=content,
            error=error)

    def get(self):
        self.render_post()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            b = Blog(subject=subject, content=content)
            b.put()
            post_id = b.key().id()

            # must redirect to a permalink based on entity ID
            self.redirect("/blog/" + str(post_id))

        else:
            error = "Enter both subject and content."
            self.render_post(subject, content, error)


class NewPostReview(Handler, Blog):
    def get(self, post_id):
        new_post_id = int(post_id)
        new_post = Blog.get_by_id(new_post_id)

        self.render("reviewpost.html", new_post=new_post)


class BlogHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

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

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()  # email is optional

    # decorators (static procedures)
    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
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
        self.render("signup.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

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

        if self.email and not valid_email(self.email):
            params['err_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    def done(self):
        # verify the user does not already exist
        u = User.by_name(self.username)

        if u:
            msg = 'User already exists'
            self.render('signup.html', err_name=msg)
        else:
            u = User.register(self.username,
                              self.password,
                              self.email)
            u.put()

            self.login(u)
            self.redirect('welcome')


class Login(BlogHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('welcome')
        else:
            msg = 'Invalid login'
            self.render('login.html', err=msg)


class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('signup')


class Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('signup')


class BlogAPI(Handler):
    # generate json from the main page
    def write_json(self):
        all_posts = db.GqlQuery("SELECT * FROM Blog "
                                "ORDER BY created DESC")

        # example: content = all_posts[0].content
        j = ''.join(json.dumps([{'content': post.content,
                                 'subject': post.subject,
                                 'created': str(post.created),
                                 'last_modified': str(post.created)}])
                    for post in all_posts)

        return j

    def get(self):
        # set the content type
        self.response.headers[
            'Content-Type'] = 'application/json; charset=UTF-8'
        self.response.write(self.write_json())


class NewPostAPI(NewPostReview):
    pass


# urls
application = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/blog/newpost', NewPost),
    ('/blog/(\d+)', NewPostReview),
    ('/blog/signup', Register),
    ('/blog/welcome', Welcome),
    ('/blog/login', Login),
    ('/blog/logout', Logout),
    ('/blog/.json', BlogAPI),
    ('/blog/(\d+).json', NewPostAPI)
], debug=True)
