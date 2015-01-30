import string
import re


def found_rot13(s):
    convert = string.maketrans(
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

    return string.translate(s, convert)


def rot13(s):

    uc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLM'
    lc = 'abcdefghijklmnopqrstuvqxyzabcdefghijklm'

    tmp = []
    other_chars = r'[0-9]'

    for char in s:

        if char.isupper():
            index = uc.find(char)
            char = uc[index + 13]
            tmp.append(char)

        if char.islower():
            index = lc.find(char)
            char = lc[index + 13]
            tmp.append(char)

        if re.match(char, other_chars):
            tmp.append(char)

    return ''.join(tmp)

print rot13('HelLo 123')
