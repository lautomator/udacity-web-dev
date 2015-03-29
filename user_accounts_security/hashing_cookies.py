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


def make_secure_val(s):
    result = s + "," + str(hash_str(s))
    return result

# Quiz 2
# -----------------
# User Instructions
#
# Implement the function check_secure_val, which takes a string of the format
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None


def check_secure_val(h):
    if hash_str(h[0]) == h[2:]:
        return h[0]

print check_secure_val('5,e4da3b7fbbce2345d7772b0674a318d5')
