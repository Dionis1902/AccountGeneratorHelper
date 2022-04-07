import random
import string

LETTERS = string.ascii_letters + '1234567890'


def random_string():
    return ''.join([random.choice(LETTERS) for _ in range(12)])