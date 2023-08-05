import random

from random_quote_generator.quotes import quotes


def get_quote() -> dict:
    """
    Get random quote

    :return: selected quote
    :rtype: dict
    """
    return random.choice(quotes)
