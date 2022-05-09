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

WEBHOOK_HOST = os.environ['WEBHOOK_HOST']  # Domain name or IP addres which your bot is located.
WEBHOOK_PORT = int(os.environ['PORT'])  # Telegram Bot API allows only for usage next ports: 443, 80, 88 or 8443
WEBHOOK_URL_PATH = os.environ['WEBHOOK_URL_PATH']  # Part of URL

WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_URL_PATH}"

# Web app settings:
#   Use LAN address to listen webhooks
#   Use any available port in range from 1024 to 49151 if you're using proxy, or WEBHOOK_PORT if you're using direct webhook handling
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001

loop = asyncio.get_event_loop()
bot = Bot(token=os.environ['TG_BOT_TOKEN'], loop=loop)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())
