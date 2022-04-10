"""client_kb

Client keyboard handler file.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_keyboard(answers):
    """Function to create keyboard.
    :param answers: list of strings for answers.
    :return keyboard markup
    """
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    for answer in answers:
        kb_client.add(KeyboardButton(answer))
    return kb_client

def create_movement_keyboard(refusal):
    """Function to create keyboard for movement.
    :param refusal: message when user don't want to locate 'em
    :return keyboard markup
    """
    geo_button = KeyboardButton('Поделиться геолокацией', request_location=True)
    no_geo_button = KeyboardButton(refusal)
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_client.row(geo_button, no_geo_button)  # in one row
    return kb_client
