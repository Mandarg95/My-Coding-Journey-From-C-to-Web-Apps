from cs50 import get_float


def main():

    Coin = 0

    while True:
        Owed = int(get_float("Change: ") * 100)

        if Owed > 0:
            break

    Coin = CoinCounter(Owed, Coin)

    print(Coin)


def CoinCounter(a, b):
    Quarter = 25
    Dimes = 10
    Nickels = 5
    pen = 1

    for i in range(a):
        if a >= Quarter:
            a = a - Quarter
            b += 1
        elif a >= Dimes:
            a = a - Dimes
            b += 1
        elif a >= Nickels:
            a = a - Nickels
            b += 1
        elif a >= pen:
            a = a - pen
            b += 1

    return b


main()
