import math
from decimal import Decimal

def main():
    for n in range(365):
        x = 1 - (Decimal(Decimal(math.factorial(365))/(Decimal(365**n)*Decimal(math.factorial(365-n)))))
        if x > Decimal(0.7):
            print(n)
            break


if __name__ == "__main__":
    main()