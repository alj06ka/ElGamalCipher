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


def is_prime(num):
    """
    Function of checking if number is prime. It's pre-checking function before
    running Miller-Rabin's prime number checking algorithm
    :param num: Number for prime checking
    :return: True if number is prime, else False
    """
    if num < 2:
        return False

    low_primes = list(primes_sieve(1000))
    if num in low_primes:
        return True

    for prime in low_primes:
        if not (num % prime):
            return False

    # If all else fails, call rabinMiller() to determine if num is a prime.
    return rabin_miller(num)


def generate_large_prime(key_size=1024):
    """
    Generating large prime number with defined size of bits
    :param key_size: size of number to generate (in bits)
    :return: generated prime number
    """
    while True:
        num = random.randrange(2**(key_size-1), 2**key_size)
        if is_prime(num):
            return num
