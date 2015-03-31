import random
import string

# implement the function make_salt() that returns a string of 5 random
# letters use python's random module.
# Note: The string package might be useful here.


def make_salt():
    salt = []
    counter = 0

    while counter < 5:
        a = random.randint(65, 122)
        salt.append(chr(a))
        counter += 1

    # result = string.join(string.replace(str(salt), ', ', ''), '')
    return salt
    # return string.strip(result, '[]')

print make_salt()


# my solution
# def make_salt():
#     salt = []
#     random_sample = random.sample(range(0, 9), 5)

#     salt = [str(i) for i in random_sample]

#     return ''.join(salt)
