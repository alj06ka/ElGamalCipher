import random


def primes_sieve(limit):
    """
    Finding array of prime numbers in range from 0 to limit
    :param limit: max value of number to find prime
    :return: list of prime numbers
    """
    a = [True] * limit
    a[0] = a[1] = False

    for (i, is_num_prime) in enumerate(a):
        if is_num_prime:
            yield i
            for n in range(i*i, limit, i):
                a[n] = False


def rabin_miller(num):
    """
    Implementation of Miller-Rabin's algorithm of checking if number is pseudo-prime
    :param num: number to check
    :return: True if number if prime, else false
    """
    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s // 2
        t += 1

    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True



