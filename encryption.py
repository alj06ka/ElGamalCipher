import ElGamalCipher.primes as prime
from random import randrange, choice
from os.path import isfile

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
        self.is_keys_configured = False

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

        self.is_keys_configured = True
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

    def encrypt_file(self, input_file_name='', output_file_name=''):
        """
        Encrypts input_file_name file using ElGamal cipher
        :param input_file_name: path to input file
        :param output_file_name: path to output file
        :return: 1 if success
        """
        # Checking input and output file
        assert input_file_name and isfile(input_file_name), "Input file wasn't selected!"
        assert output_file_name, "Output file wasn't selected!"

        # Encrypting file and saving result
        alpha = pow(self.keys['public']['g'], self.keys['session'], self.keys['public']['p'])
        try:
            with open(output_file_name, 'wb') as f:
                for _byte in open(input_file_name, 'rb').readline():
                    beta = (self.keys['public']['g'] ** self.keys['session'])*_byte % self.keys['public']['p']
                    f.write(alpha)
                    f.write(beta)
        except Exception:
            debug_message(f"Error occurred while encrypting file ({Exception})")
            raise AssertionError(f"File encrypting error! ({Exception})")

        return 1

    def decrypt(self, input_file_name='', output_file_name=''):
        """
        Decrypts file using ElGamal cipher
        :param input_file_name: path to input file
        :param output_file_name: path to output file
        :return: 1 if successful
        """

        def _open_file_binary(filename):
            """
            Reading file byte to byte
            :param filename: path to file to read
            :return: generator of file bytes as integer values
            """
            for _byte in open(filename, 'rb').read():
                yield _byte

        # Checking if input and output files selected right
        assert input_file_name and isfile(input_file_name), "Input file wasn't selected!"
        assert output_file_name, "Output file wasn't selected!"
        with open(output_file_name, 'wb') as output_file:
            # To iterate file as int values, I'm using generator
            input_file = _open_file_binary(input_file_name)
            try:
                alpha = input_file.__next__()
                beta = input_file.__next__()
            except StopIteration:
                raise AssertionError("Input file is empty! Nothing to decrypt.")
            while alpha and beta:
                message_byte = (beta * (alpha ** self.keys['private'])**(-1)) % self.keys['public']['p']
                output_file.write(message_byte)
                try:
                    alpha = input_file.__next__()
                    beta = input_file.__next__()
                except StopIteration:
                    alpha = 0
                    beta = 0
        return 1
