import random
import string

def random_string(length: int) -> str:
    """Generate a random strength of length."""
    print(length)
    return ''.join([random.choice(string.ascii_letters) for _ in range(length)])
