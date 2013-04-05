import string

def rot13(s):
    result = ""
    for c in s:
        if c not in string.ascii_letters:
            result += c
            continue
        do_capitalize = False
        if c in string.ascii_uppercase:
            do_capitalize = True
        rot = (ord(c.lower()) + 13) % 123
        if rot < 96:
            rot += 97
        if do_capitalize:
            result += chr(rot).upper()
        else:
            result += chr(rot)
    return result