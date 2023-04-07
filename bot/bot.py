"""bot

Main bot python file.
"""

from create_bot import dp, bot, logging, WEBAPP_HOST, WEBAPP_PORT #, WEBHOOK_URL, WEBHOOK_PATH
from aiogram.utils.executor import start_webhook, start_polling
from handlers import client


async def on_startup(_):
    """Function when bot starts up
    """
    client.register_client_handlers(dp)
    #await bot.set_webhook(WEBHOOK_URL)
    logging.info("Bot is online")


async def on_shutdown(app):
    """Graceful shutdown. This method is recommended by aiohttp docs.
    :param app: Applicaiton context
    """
    #await bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.info("Bot is offline")


if __name__ == "__main__":
    '''start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )'''
    start_polling(dp,
                  on_startup=on_startup,
                  on_shutdown=on_shutdown,
                  skip_updates=True)