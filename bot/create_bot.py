"""create_bot

Bot creation file.
"""

import os
from aiogram import Bot, Dispatcher
# State machine stores in RAM
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

bot = Bot(token=os.environ['TG_BOT_TOKEN'])
dp = Dispatcher(bot, storage=storage)