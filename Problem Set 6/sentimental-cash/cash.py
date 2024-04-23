import cs50 as cs


def csh():
    while True:
        x = cs.get_float("Change: ")
        if x < 0:
            continue
        else:
            return f"{x: .2f}"


s = csh()


def cash(s):
    a = s.split(".")
    d = int(a[0])*4
    c1 = int(a[1])

    coin = 0
    while c1 >= 25:
        c1 -= 25
        coin += 1

    while c1 >= 10:
        c1 -= 10
        coin += 1

    while c1 >= 5:
        c1 -= 5
        coin += 1

    while c1 >= 1:
        c1 -= 1
        coin += 1
    return coin+d


print(cash(s))
