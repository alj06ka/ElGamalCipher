import ElGamalCipher.primes as prime
from random import randrange, choice

DEFAULT_KEY_PATH = 'elgamal_key'


class ElGamal:
    def __init__(self, keys=None):
        self.keys = keys

    def set_keys(self, keys=None, key_size=1024):
        """
        Setting key values from set parameters
        :param keys: dict that includes public, private and session key
        :param key_size: size (in bits) of key to generate
        :return: keys
        """
        self.keys = keys
        # Generating public key p num if it's not set
        if not self.keys['public']['p']:
            self.keys['public']['p'] = prime.generate_large_prime(key_size)
        p_num = self.keys['public']['p']

        # Finding primitive root
        self.keys['public']['g'] = choice(prime.primitive_roots(p_num))

        # Setting private key
        if not self.keys['private']:
            self.keys['private'] = randrange(2, p_num-1)

        # Calculating y public key
        self.keys['public']['y'] = pow(self.keys['public']['g'], self.keys['private'], p_num)

        # Finding session key if it's not set
        while not self.keys['session']:
            prime_key = prime.generate_large_prime(randrange(2, key_size+1))
            self.keys['session'] = prime_key if (prime_key < p_num) and (prime.gcd(prime_key, p_num) == 1) else 0

        return self.keys
