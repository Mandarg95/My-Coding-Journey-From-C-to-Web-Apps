from cs50 import get_int


def main():

    while True:
        hight = get_int(("Hight: "))
        if hight > 0 and hight < 9:
            break

    peramit(hight)


def peramit(n):
    for i in range(n):
        for space in range(n - i - 1):
            print(" ", end='')
            
        for LeftSide in range(i + 1):
            print("#", end='')

        for MidSpace in range(2):
            print(" ", end='')

        for RightSide in range(i + 1):
            print("#", end='')
        print()


main()
