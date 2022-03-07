"""create_bot

Bot creation file.
"""

import os
from aiogram import Bot, Dispatcher

bot = Bot(token=os.environ['TG_BOT_TOKEN'])
dp = Dispatcher(bot)