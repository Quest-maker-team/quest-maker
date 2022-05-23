"""create_bot

Bot creation file.
"""

import logging
import asyncio

import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


storage=MemoryStorage()

TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
WEBHOOK_HOST = os.environ['WEBHOOK_HOST']  # Domain name or IP addres which your bot is located.
WEBHOOK_PATH = f"/webhook/{TG_BOT_TOKEN}"  # Part of URL

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Web app settings:
#   Use LAN address to listen webhooks
#   Use any available port in range from 1024 to 49151 if you're using proxy, or WEBHOOK_PORT if you're using direct webhook handling
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

loop = asyncio.get_event_loop()
bot = Bot(token=TG_BOT_TOKEN, loop=loop)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())
