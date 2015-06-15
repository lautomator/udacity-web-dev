import hashlib


def hash_str(s):
    return hashlib.md5(s).hexdigest()

# Quiz 1
# -----------------
# User Instructions
#
# Implement the function make_secure_val, which takes a string and returns a
# string of the format:
# s,HASH


# my solution
# def make_secure_val(s):
#     result = s + "," + str(hash_str(s))
#     return result

# Quiz 2
# -----------------
# User Instructions
#
# Implement the function check_secure_val, which takes a string of the format
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None

def make_secure_val(s):
    return "%s,%s" % (s, hash_str(s))


def check_secure_val(h):
    val = h.split(',')[0]
    if h == make_secure_val(val):
        return val

print hash_str('5')
print check_secure_val('5,e4da3b7fbbce2345d7772b0674a318d5')
