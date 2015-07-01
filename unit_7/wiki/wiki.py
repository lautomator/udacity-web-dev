import os
import re
import random
import hashlib
import hmac
import json
import logging
from string import letters

import webapp2
import jinja2

from google.appengine.api import memcache
from google.appengine.ext import db

# =====================
# templating directives
# =====================
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

secret = 'nvSqlliCsiKCcfds'

# =============================
# global regexs for validation:
# =============================
_user_re = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
_pw_re = re.compile(r'^.{3,20}$')
_email_re = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


# ==============================
# user and validation procedures
# ==============================
def valid_username(s):
    return _user_re.match(s)


def valid_password(s1):
    return _pw_re.match(s1)


def valid_verify(s1, s2):
    return s1 == s2


def valid_email(s):
    return _email_re.match(s)


def users_key(group='default'):
    return db.Key.from_path('users', group)


# ========
# security
# ========
def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, pw, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, pw, salt)


# =========
# appengine
# =========
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


# =========
# memchache
# =========
def get_articles(update=False):
    key = 'articles'
    all_articles = memcache.get(key)

    if all_articles is None or update:
        logging.error("DB QUERY")

        all_articles = db.GqlQuery("SELECT * FROM Wiki")

        all_articles = list(all_articles)
        memcache.set(key, all_articles)

    return all_articles


def flush():
    key = 'articles'
    all_articles = memcache.get(key)

    del all_articles[:]

    get_articles(True)


class Flush(Handler):
    def get(self):

        # flush the cache
        flush()

        self.redirect(page_url)


# ====
# wiki
# ====
class Wiki(db.Model):
    page_name = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class WikiHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    # cookie directives
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


class WikiPage(Handler, WikiHandler):
    def render_wiki_page(self,
                         username="",
                         page_name="",
                         content="",
                         created="",
                         error=""):

        articles = get_articles()
        username = self.user.name

        p = str(page_name) in articles

        content = p

    # for i in articles:
    #        if str(i.page_name) == page_name:
    #            content = i.content
    #            break

        self.render(
            "page.html",
            content=content,
            created=created,
            error=error,
            login_url=login_url,
            logout_url=logout_url,
            signup_url=signup_url,
            edit_url=edit_url,
            articles=articles,
            username=username,
            page_name=page_name)

    def get(self, page_name):
        if self.user:
            self.render_wiki_page(page_name=page_name)
        else:
            self.redirect(login_url)


class EditPage(Handler, WikiHandler):
    def render_article(self,
                       username="",
                       content="",
                       page_name="",
                       error=""):
        self.render(
            "edit.html",
            username=self.user.name,
            content=content,
            page_name=page_name,
            error=error,
            logout_url=logout_url)

    def get(self, page_name):
        if self.user:
            self.render_article()
        else:
            self.redirect(login_url)

    def post(self, page_name):
        content = self.request.get("content")

        if content:
            b = Wiki(page_name=page_name, content=content)
            b.put()

            # update the cache
            get_articles(True)

            article_subject = b.page_name

            # render the new page
            self.render_article(page_name=article_subject,
                                content=content)

        else:
            error = "Enter some content."
            self.render_article(error=error)


# class Test(Handler, Wiki):
#     def get(self, article_name):
#         # new_article_name = int(article_name)
#         # article_id = Wiki.get_by_id(new_article_name)

#         self.render("page.html",
#                     page_name=article_name,
#                     content=self.page_name,
#                     edit_url='')


# ============
# login/signup
# ============
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


class Signup(WikiHandler):

    def get(self):
        self.render("signup.html",
                    login_url=login_url)

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
            self.redirect(page_url)


class Login(WikiHandler):
    def get(self):
        self.render('login.html',
                    signup_url=signup_url)

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect(page_url)
        else:
            msg = 'Invalid login'
            self.render('login.html',
                        err=msg,
                        signup_url=signup_url)


class Logout(WikiHandler):
    def get(self):
        self.logout()
        self.redirect(login_url)


# ===
# API
# ===
# TODO: These may not be needed
class WikiAPI(WikiPage):
    # generate json from the main page
    def wiki_json(self):
        all_articles = get_articles()

        # example: content = all_articles[0].content
        j = "[" + ', '.join(json.dumps({'content': post.content,
                                        'created': str(post.created),
                                        'last_modified': str(post.created)})
                            for post in all_articles) + "]"
        return j

    def get(self):
        # set the content type
        self.response.headers[
            'Content-Type'] = 'application/json; charset=UTF-8'
        self.response.write(self.wiki_json())


class NewPostAPI(Handler, Wiki):
    def get(self, post_id):
        new_post_id = int(post_id)
        new_post = Wiki.get_by_id(new_post_id)

        j = json.dumps([{'content': new_post.content,
                         'created': str(new_post.created),
                         'last_modified': str(new_post.created)}])

        self.response.headers[
            'Content-Type'] = 'application/json; charset=UTF-8'
        self.response.write(j)

# ====================
# urls and url mapping
# ====================
page_url = '/'
login_url = '/login'
logout_url = '/logout'
signup_url = '/signup'
edit_url = '/_edit'

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

application = webapp2.WSGIApplication([
    (signup_url, Signup),
    (login_url, Login),
    (logout_url, Logout),
    (edit_url + PAGE_RE, EditPage),
    (PAGE_RE, WikiPage),
], debug=True)
