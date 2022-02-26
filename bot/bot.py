"""bot

Main bot python file.
"""

import os
import logging
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=os.environ['TG_BOT_TOKEN'])
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)