"""client

Client commands handler file.
"""

from aiogram import types, Dispatcher


async def cmd_start(message: types.Message):
    await message.answer('Это бот для игры в квесты, созданные при помощи сервиса QuestCreator.')


def activate_quest(name):
    return name == "zero"


async def cmd_quest(message: types.Message):
    arguments = message.get_args()
    if len(arguments) == 0:
        await message.reply('Требуется аргумент команды: идентификатор квеста')
        return
    if activate_quest(arguments):
        await message.answer('Квест "' + arguments + '" начат')
    else:
        await message.reply('Квест "' + arguments + '" не найден')


async def cmd_end(message: types.Message):
    await message.answer('Квест завершён')


async def echo(message: types.Message):
    await message.answer(message.text)


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start', 'help'])
    dp.register_message_handler(cmd_quest, commands='quest')
    dp.register_message_handler(cmd_end, commands='end')
    dp.register_message_handler(echo)