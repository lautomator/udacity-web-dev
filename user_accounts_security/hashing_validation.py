import hashlib
import random
import string


def make_salt():
    return ''.join(random.choice(string.letters) for x in range(5))

# Implement the function valid_pw() that returns True if a user's password
# matches its hash. You will need to modify make_pw_hash.


def make_pw_hash(name, pw):
    salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)


def valid_pw(name, pw, h):
    hashed_pw = make_pw_hash(name, pw)
    return hashed_pw

h = make_pw_hash('spez', 'hunter2')
print h
print valid_pw('spez', 'hunter2', h)
