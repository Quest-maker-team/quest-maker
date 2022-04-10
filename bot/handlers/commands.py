"""commands

Contains bot commands lists.
"""

from aiogram import Bot, types


async def set_commands(bot: Bot):
    """Set commands to display.
    :param dp: dispatcher
    """
    await bot.set_my_commands([
        types.BotCommand("help", "Помощь"),
        types.BotCommand("quest", "Начать квест"),
        types.BotCommand("end", "Закончить квест"),
        types.BotCommand("tip", "Получить подсказку"),
        types.BotCommand("score", "Узнать количество баллов"),
        types.BotCommand("skip", "Попытаться пропустить точку"),
    ])