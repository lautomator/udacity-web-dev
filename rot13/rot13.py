import webapp2
import cgi
import re


form = """
    <form method="post">
        <label>
            <pre>Enter some text to ROT13:</pre>

            <textarea name="text" cols="56" rows="8">%(value)s</textarea>
        </label>

        <br>
        <input type="submit">
    </form>
"""


class MainPage(webapp2.RequestHandler):

    def write_form(self, form_value=''):

        self.response.write(form % {'value': form_value})

    def get(self):

        self.write_form()

    def post(self):

        user_entry = escape_html(self.request.get('text'))

        entry = rot13(user_entry)

        self.write_form(entry)


# URLs
application = webapp2.WSGIApplication([('/', MainPage)], debug=True)


def escape_html(s):

    return cgi.escape(s, quote=True)


def rot13(s):

    uc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLM'
    lc = 'abcdefghijklmnopqrstuvqxyzabcdefghijklm'

    tmp = []

    for char in s:

        if char.isupper():
            index = uc.find(char)
            char = uc[index + 13]
            tmp.append(char)

        if char.islower():
            index = lc.find(char)
            char = lc[index + 13]
            tmp.append(char)

        if char == ' ' or char == '' or char == '\n' or char == '\t':
            tmp.append(char)

    return ''.join(tmp)
