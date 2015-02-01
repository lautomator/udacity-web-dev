import webapp2
import cgi
import re


form = """<!DOCTYPE html>

<html>
    <head>
        <meta charset="utf-8">
        <title>Signup</title>
    </head>

    <body style="font-family: sans-serif">
        <h1>Signup</h1>

        <!--// the signup form //-->
        <form method="post">

            <table style="border: none; padding: 0; margin: 0">
                <tr>
                    <td>Username</td>
                    <td>
                        <input type="text" name="username"
                            value="%(username)s">
                        <span style="color: red">%(err_name)s</span>
                    </td>
                </tr>

                <tr>
                    <td>Password</td>
                    <td>
                        <input type="password" name="password"
                            value="%(password)s">
                        <span style="color: red">%(err_password)s</span>
                    </td>
                </tr>

                <tr>
                    <td>Verify Password</td>
                    <td>
                        <input type="password" name="verify"
                            value="%(verify)s">
                        <span style="color: red">%(err_verify)s</span>
                    </td>
                </tr>

                <tr>
                    <td>Email (optional)</td>
                    <td>
                        <input type="text" name="email" value="%(email)s">
                        <span style="color: red">%(err_email)s</span>
                    </td>
                </tr>
                <tr>
                    <td colspan="2"><input type="submit" value="Submit"></td>
                </tr>
            </table>
        </form>
    </body>
</html>
"""


class MainPage(webapp2.RequestHandler):

    def write_form(
        self,
        err_name='',
        err_password='',
        err_verify='',
        err_email='',
        username="",
        password="",
        verify="",
        email=""
    ):

        self.response.write(form % {
            'err_name': err_name,
            'err_password': err_password,
            'err_verify': err_verify,
            'err_email': err_email,
            'username': escape_html(username),
            'password': escape_html(password),
            'verify': escape_html(verify),
            'email': escape_html(email)
        })

    def get(self):

        self.write_form()

    def post(self):

        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
#        user_email = self.request.get('email')

        username = valid_username(user_username)
        password = valid_password(user_password)
        verify = valid_verify(password, user_verify)

        if not username:
            err_name = "That's not a valid username."

        if not password:
            err_password = "That's not a valid password"

        if password and not verify:
            err_verify = "Password does not match."

        else:
            self.redirect("/welcome")

        self.write_form(
            err_name=err_name,
            username=user_username,
            err_password=err_password,
            err_verify=err_verify
        )

#        if user_email:
#            email = valid_email(user_email)
#
#            if not email:
#                self.write_form(err_email="That's not a valid email.")


class WelcomeHandler(webapp2.RequestHandler):

    def get(self):

        # TODO: need to add the accepted username
        self.response.write("Welcome, ")


# URLs
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome', WelcomeHandler)
], debug=True)


# escape nasty html chars
def escape_html(s):

    return cgi.escape(s, quote=True)

# regexs for validation:
USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
PW_RE = re.compile(r'^.{3,20}$')
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


# validation procedures
def valid_username(s):
    return USER_RE.match(s)


def valid_password(s1):
    return PW_RE.match(s1)


def valid_verify(s1, s2):

    if s1 == s2:
        return s2


def valid_email(s):
    return EMAIL_RE.match(s)
