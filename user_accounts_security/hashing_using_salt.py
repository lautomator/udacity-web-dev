	import hashlib
import random
import string

# implement the function make_salt() that returns a string of 5 random
# letters use python's random module.
# Note: The string package might be useful here.


def make_salt():
    return ''.join(random.choice(string.letters) for x in range(5))

print make_salt()

# implement the function make_pw_hash(name, pw) that returns a hashed password
# of the format:
# HASH(name + pw + salt),salt
# use sha256


def make_pw_hash(name, pw):
    s = make_salt()
    h = hashlib.sha256(name + pw + s).hexdigest()
    return '%s,%s' % (h, s)

print make_pw_hash('john', 'yomma')
