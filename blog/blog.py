import os
import webapp2
import jinja2

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


class Blog(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):
    def render_front(self, subject="", content="", error=""):
        all_posts = db.GqlQuery("SELECT * FROM Blog "
                                "ORDER BY created DESC")

        # get the 10 most recent
        posts = all_posts[0:9]

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

# urls
application = webapp2.WSGIApplication([
    (r'/blog', MainPage),
    (r'/blog/newpost', NewPost),
    (r'/blog/(\d+)', NewPostReview)
], debug=True)
