# User Instructions
#
# Implement the function escape_html(s), which replaces:
# > with &gt;
# < with &lt;
# " with &quot;
# & with &amp;
# and returns the escaped string
# Note that your browser will probably automatically
# render your escaped text as the corresponding symbols,
# but the grading script will still correctly evaluate it.
#


def brute_escape_html(s):

    corrections_list = []

    for char in s:
        if char == '>':
            char = '&gt;'
        if char == '<':
            char = '&lt;'
        if char == '"':
            char = '&quot;'
        if char == '&':
            char = '&amp;'
        corrections_list.append(char)

    return ''.join(corrections_list)

print brute_escape_html('This is the < user > input " with & escape chars.')


# or use the cgi  module
import cgi


def escape_html(s):

    return cgi.escape(s, quote=True)

print escape_html('This is the < user > input " with & escape chars.')
