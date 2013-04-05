# 
# Finish the simplify function.
# Have it deal with the case where test(s1) doesn't fail
# 
# If neither s1 or s2 cause the test to fail then return 
# the original string, s.

import re

def test(s):
    print `s`, len(s)
    if re.search("<SELECT[^>]*>", s) >= 0:
        return "FAIL"
    else:
        return "PASS"

def simplify(s):
    assert test(s) == "FAIL"
    
    split = re.split("(<[^>]+>)", s)
    print split
    s1 = ''.join(split[:len(split)/2])
    s2 = ''.join(split[len(split)/2:])
    print s1, s2
    
    assert s == s1 + s2
    
    if test(s1) == "FAIL":
        return simplify(s1)
    elif test(s2) == "FAIL":
        return simplify(s2)

# UNCOMMENT TO TEST
html_input = '<SELECT>foo</SELECT>'
print simplify(html_input)
