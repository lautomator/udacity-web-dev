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

print rot13('HelLo 123 %$#\n\nsome More text    and spaces\n')
