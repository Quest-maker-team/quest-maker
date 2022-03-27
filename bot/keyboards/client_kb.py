"""client_kb

Client keyboard handler file.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_keyboard(answers):
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    for answer in answers:
        kb_client.add(KeyboardButton(answer))
    return kb_client
