#
# Finish the delta debug function ddmin
#


import re

TEST_COUNT = 0

def test(s):
    print `s`, len(s)

    s_merged = ''.join(s)

    if re.search("<SELECT[^>]*>", s_merged) >= 0:
        return "FAIL"
    else:
        return "PASS"

def ddmin(s,test):
    assert test(s) == "FAIL"

    n = 2     # Initial granularity
    while len(s) >= 2:
        start = 0
        subset_length = len(s) / n
        some_complement_is_failing = False

        while start < len(s):
            complement = s[:start] + s[start + subset_length:]
            global TEST_COUNT
            TEST_COUNT = TEST_COUNT + 1
            if test(complement) == "FAIL":
                s = complement
                n = max(n - 1, 2)
                some_complement_is_failing = True
                break

            start += subset_length

        if not some_complement_is_failing:
            if n == len(s): break
            n = min(2*n, len(s))
            if n == len(s): break

    return s

# UNCOMMENT TO TEST
html_input = ['<SELECT>','foo','</SELECT>']
print ddmin(html_input,test)
print TEST_COUNT
