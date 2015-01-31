import webapp2
import cgi


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
          <input type="text" name="username" value="%(username)s">
          <span style="color: red">%(error)s</span>
        </td>
      </tr>

      <tr>
        <td>Password</td>
        <td>
          <input type="text" name="password" value="%(password)s">
          <span style="color: red">%(error)s</span>
        </td>
      </tr>

      <tr>
        <td>Verify Password</td>
        <td>
          <input type="text" name="verify" value="%(verify)s">
          <span style="color: red">%(error)s</span>
        </td>
      </tr>

      <tr>
        <td>Email (optional)</td>
        <td>
          <input type="text" name="email" value="%(email)s">
          <span style="color: red">%(error)s</span>
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
        error='',
        username="",
        password="",
        verify="",
        email=""
    ):

        self.response.write(form % {
            'error': error,
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
        # user_verify = self.request.get('verify')
        user_email = self.request.get('email')

        # TODO: write validation functions for all
        username = user_username
        password = user_password
        email = user_email

        self.redirect("/welcome")
'''
        username = valid_username(user_username)
        password = valid_password(user_password, user_verify)
        email = valid_email(user_email)
'''

# if not (month and day and year):
#    self.write_form(
#        "That does not look valid.",
#        user_month, user_day, user_year)
# else:
#    self.redirect("/thanks")


class WelcomeHandler(webapp2.RequestHandler):

    def get(self, username):

        self.response.write("Welcome, " + username)


# URLs
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome', WelcomeHandler)
], debug=True)


# escape nasty html chars
def escape_html(s):

    return cgi.escape(s, quote=True)
