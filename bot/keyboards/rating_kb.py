"""rating_kb

Rating keyboard handler file.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


star_ch = '★'


def create_rating_keyboard(answers):
    """Function to create keyboard.
    :param answers: list of strings for answers.
    :return keyboard markup
    """
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    for len in range(1, 6):
        kb_client.add(KeyboardButton(star_ch * len))
    return kb_client

def get_rating(star_string):
    """Function to get rating.
    :param star_string: string with stars.
    :return rating or None if string is incorrect
    """
    for ch in star_string:
        if star_ch != ch:
            return None
    len = len(star_string)
    if len == 0 or len > 5:
        return None
    return len
