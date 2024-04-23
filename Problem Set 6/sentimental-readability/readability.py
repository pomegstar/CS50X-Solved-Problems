import cs50 as cs
import re


def Grade(s):
    wo = s.split(" ")
    word = len(wo)
    se = re.split(r'[.!?]', s)

    S = (len(se)-1)*100/word
    l = []

    for i in s.lower():
        if i in "abcdefghijklmnopqrstuvwxyz":
            l.append(i)

    L = (len(l)*100)/word
    ind = 0.0588 * L - 0.296 * S - 15.8
    if 1 > round(ind):
        return ("Before Grade 1")
    elif 16 <= round(ind):
        return ("Grade 16+")
    else:
        return (f"Grade {round(ind)}")


s = cs.get_string("Text: ")
print(Grade(s))
