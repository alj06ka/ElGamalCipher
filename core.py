from ElGamalCipher.settings import DEBUG


def debug_message(message):
    """
    Printing debug message if DEBUG mode is enabled
    :param message:
    :return:
    """
    if DEBUG:
        print(f'[DEBUG] {message}')


def get_file_bits(src_file, num_of_bits):
    """
    Function that represents file as sequence of bits
    :param src_file: path to selected file
    :param num_of_bits: quantity of bits needed to return
    :return: string that consists list of :num_of_bits: bits
    """
    def _convert_byte_to_bits(_byte):
        """
        Converts byte to string that consists sequence of bits
        :param _byte:
        :return: sequence of bits
        """
        _list_of_bits = []
        for _ in range(8):
            _list_of_bits.append(str(_byte & 1))
            _byte >>= 1
        return ''.join(list(reversed(_list_of_bits)))

    _num_of_bits = 0
    list_of_bits = []
    file_byte = 1
    with open(src_file, 'rb') as f:
        while _num_of_bits < num_of_bits and file_byte:
            file_byte = f.read(1)
            if file_byte:
                list_of_bits.append(_convert_byte_to_bits(file_byte[0]))
            _num_of_bits += 8
    return ' '.join(list_of_bits)
