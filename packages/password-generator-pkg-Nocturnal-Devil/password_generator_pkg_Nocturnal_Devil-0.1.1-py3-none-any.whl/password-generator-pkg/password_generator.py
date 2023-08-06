"""
Password Generator
"""

from hashlib import md5
from getpass import getpass
from pyperclip import copy


def generate_hash(password: str):
    """
    Generate MD5 hash from given password

    :param password: Password to create a hash from
    :return: Hashed password
    """
    return md5(password.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    try:
        input_password = getpass(prompt='Enter your password: ')
        copy(generate_hash(input_password))
    except KeyboardInterrupt:
        print()  # Fancier in console
