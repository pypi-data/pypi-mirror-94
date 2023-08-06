# Fermat Prime Factorization method with Python

import math
from decimal import Decimal


def fermat_factorization(n):
    """
    This function takes single integer as parameter and returns 2 factors of n based on Fermat Factorization Technique.
    :param n: int
    :return: int,int
    """
    if n % 2 == 0:
        return n // 2, 2
    sqrt_num = math.sqrt(n)  # calculating square root

    i = math.ceil(sqrt_num)  # rounding off to nearest integer greater than sqrt_num

    j = math.sqrt(i ** 2 - n)

    a, b = 0, 0

    if j.is_integer():  # check if x is integer before 1st iteration
        j = int(j)
        a = i + j
        b = i - j
    else:
        while isinstance(j, float):
            i += 1
            j = math.sqrt(i ** 2 - n)
            # print(i, j)
            if Decimal(j) % 1 == 0:
                # print(i, j)
                a = (int(i + j))
                b = (int(i - j))
                # print('Factors: ', int(i + j), 'x', int(i - j))
                break
    return a, b


def prime_check(n):
    """
    Checks if input parameter is a prime number or not by using Fermat Factorization method
    :param n: integer
    :return: bool
    """
    i, j = fermat_factorization(n)
    if (i == n and i != 1) or (i == 1 and j == 2):
        return True
    else:
        return False


def primes_in_range(n1, n2):
    """
    This function takes 2 integer inputs and returns a list of prime numbers between them (both numbers inclusive)
    :param n1: integer
    :param n2: integer
    :return: list
    """
    prime_list = []
    for i in range(n1, n2 + 1):
        if prime_check(i):
            prime_list.append(i)
    return prime_list


if __name__ == '__main__':
    number = int(input('Enter Integer to Factorize: '))
    x, y = fermat_factorization(number)
    print(x, "\t", y)
    p1 = primes_in_range(1, 50)
    print(p1)
