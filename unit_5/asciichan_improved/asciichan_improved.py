import os
import webapp2
import jinja2
import urllib2
from xml.dom.minidom import parseString

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


IP_URL = "http://api.hostip.info/?p="


def get_coords(ip):
    url = IP_URL + ip
    content = None

    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        # you could log errors here if you wanted to
        return

    if content:
        # parse xml and find the coordinates
        pass


class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art "
                           "ORDER BY created DESC")

        self.render(
            "front.html",
            title=title,
            art=art,
            error=error,
            arts=arts)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title=title, art=art)

            # lookup user coordinates from ip address
            # if we have coordinates, add them to the page

            a.put()
            self.redirect("/")
        else:
            error = "Enter a title and artwork."
            self.render_front(title, art, error)

application = webapp2.WSGIApplication([('/', MainPage)], debug=True)
