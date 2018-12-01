import ElGamalCipher.primes as prime
from random import randrange, choice

DEFAULT_KEY_PATH = 'elgamal_key'
DEBUG = True


def debug_message(message):
    """
    Printing debug message if DEBUG mode is enabled
    :param message:
    :return:
    """
    if DEBUG:
        print(f'[DEBUG] {message}')
    return


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

    def save_keys(self, save_path=DEFAULT_KEY_PATH):
        """
        Saving encryption keys to file
        :param save_path: path to save keys
        :return: 1 if saving successful else 0
        """
        try:
            with open(f'{save_path}/id_elgamal', 'w') as f:
                f.write(self.keys['private'])
            with open(f'{save_path}/id_elgamal.pub', 'w') as f:
                f.write(self.keys['public']['p']+'\n')
                f.write(self.keys['public']['g']+'\n')
                f.write(self.keys['public']['y']+'\n')
            debug_message('Saving complete!')
            return 1
        except Exception:
            debug_message(f'Saving error! ({Exception})')
            return 0

    def load_keys(self, load_path=DEFAULT_KEY_PATH):
        """
        Loading keys from file
        :param load_path: path that includes files with keys
        :return: dict with keys if successful else 0
        """
        try:
            with open(f'{load_path}/id_elgamal', 'r') as f:
                f.read(self.keys['private'])
            with open(f'{load_path}/id_elgamal.pub', 'r') as f:
                self.keys['public']['p'] = f.readline()
                self.keys['public']['g'] = f.readline()
                self.keys['public']['y'] = f.readline()
            debug_message('Loading successful!')
            return self.keys
        except FileNotFoundError:
            debug_message(f'Loading error! ({Exception})')
            return 0
