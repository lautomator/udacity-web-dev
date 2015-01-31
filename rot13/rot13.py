import webapp2
import cgi
import re


form = """<!DOCTYPE html>

<html>
  <head>
    <title>Rot13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>

    <form method="post">
        <textarea name="text" cols="56" rows="8">%(value)s</textarea>

        <br>
        <input type="submit">
    </form>
  </body>

</html>
"""


class MainPage(webapp2.RequestHandler):

    def write_form(self, form_value=''):

        self.response.write(form % {'value': form_value})

    def get(self):

        self.write_form()

    def post(self):

        user_entry = self.request.get('text')

        entry = rot13(user_entry)

        self.write_form(escape_html(entry))


# URLs
application = webapp2.WSGIApplication([(
    '/rot13/',
    MainPage)], debug=True)


def escape_html(s):

    return cgi.escape(s, quote=True)


def rot13(s):

    uc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLM'
    lc = 'abcdefghijklmnopqrstuvqxyzabcdefghijklm'

    conversion = []
    other_chars = r'[\d\s\W]'

    for char in s:

        if char.isupper():
            index = uc.find(char)
            char = uc[index + 13]
            conversion.append(char)

        if char.islower():
            index = lc.find(char)
            char = lc[index + 13]
            conversion.append(char)

        if re.match(other_chars, char):
            conversion.append(char)

    return ''.join(conversion)
