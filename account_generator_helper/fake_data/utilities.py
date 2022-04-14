import random
import string


def get_password(length: int = 16, upper_case=True, numbers=True, special_symbols=True) -> str:
    """
    Function for generate passwords.

    :param length: Length of password.
    :param upper_case: Use upper case.
    :param numbers: Use numbers.
    :param special_symbols: Use special symbols.
    :return: Password.
    """
    data = {'upper_case': string.ascii_uppercase, 'numbers': string.digits, 'special_symbols': string.punctuation}
    _data = locals()
    letters = string.ascii_lowercase + ''.join([data[key] for key in list(_data)[1:4] if _data[key]])
    return ''.join([random.choice(letters) for _ in range(length)])