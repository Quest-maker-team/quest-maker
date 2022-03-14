"""bot

Main bot python file.
"""

from aiogram import executor
from create_bot import dp
from handlers import client

async def on_startup(_):
    """Function when bot starts up
    """
    print("Bot is online")


if __name__ == "__main__":
    client.register_client_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)