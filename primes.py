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


