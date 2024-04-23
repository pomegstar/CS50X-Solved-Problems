def get_int():
    while True:
        n = input("Height: ")
        try:
            if 0 < int(n) < 9:
                return int(n)
            else:
                continue
        except ValueError:
            continue


n = get_int()
for i in range(n):
    print((n-i-1)*" "+(i+1)*"#")
