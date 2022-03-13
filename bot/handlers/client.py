"""client

Client commands handler file.
"""

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestPoint:
    def __init__(self, msg):
        self.msg = msg
        self.next_points = None


    def load_next_points(self, points):
        self.next_points = points


    def get_next(self, point_name):
        if point_name in self.next_points:
            return self.next_points[point_name]
        return None


def get_quest_info(name):
    start_msg = 'Привет. Это нулевой квест проекта QuestMaker.'
    end_msg = 'До свидания от нулевого квеста.'
    
    point_cormen = QuestPoint("Осуждаем.")
    point_dijkstra = QuestPoint("Одобряем.")
    point_novikov = QuestPoint("Гиперодобряем.")

    point_dm_question = QuestPoint("Ваш любимый исследователь дискретной математики из "
        "Эдсрега А. Дейкстры, Томаса Г. Кормена и Фёдора А. Новикова?")
    point_dm_question.load_next_points({'Кормен': point_cormen, 'Дейкстра': point_dijkstra, 'Новиков': point_novikov})

    point_arithmetic = QuestPoint("2+2?")
    point_arithmetic.load_next_points({"4": point_dm_question})

    return (start_msg, point_arithmetic, end_msg)


class Quest:
    def __init__(self, name):
        self.name = name
        (self.start_msg, self.cur_point, self.end_msg) = get_quest_info(name)


    def next_point(self, message):
        point = self.cur_point.get_next(message)
        if point is None:
            return (False, "Неправильный ответ.")
        self.cur_point = point
        if point.next_points is None:
            return (True, point.msg)
        return (False, point.msg)


class QuestStates(StatesGroup):
    naming = State()
    session = State()


async def cmd_start(message: types.Message):
    await message.answer('Это бот для игры в квесты, созданные при помощи сервиса QuestCreator.')


def activate_quest(name):
    return name == "zero"


async def cmd_quest(message: types.Message):
    await QuestStates.naming.set()
    await message.answer('Введите имя квеста.')


async def cmd_end(message: types.Message):
    await message.answer('Квест завершён.')


async def name_quest(message: types.Message, state: FSMContext):
    if activate_quest(message.text):
        async with state.proxy() as data:
            data['quest'] = Quest(message.text)
        await QuestStates.next()
        await message.answer('Квест "' + message.text + '" начат. Чтобы закончить напишите /end')
        await message.answer(data['quest'].cur_point.msg)
    else:
        await message.reply('Квест "' + message.text + '" не найден')
        await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    currentState = await state.get_state()
    if currentState is None:
        return
    await state.finish()


async def quest_proc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        (quest_ends, msg) = data['quest'].next_point(message.text)
        await message.answer(msg)
        if quest_ends == True:
            await message.answer(data['quest'].end_msg)
            await state.finish()
            await message.answer('Квест "' + data['quest'].name + '" закончен.')


async def warning(message: types.Message):
    await message.answer('Выберите квест командой /quest.')


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start', 'help'])
    dp.register_message_handler(cmd_quest, commands='quest')
    dp.register_message_handler(cmd_end, commands='end')
    dp.register_message_handler(cancel_handler, state='*', commands="end")
    dp.register_message_handler(name_quest, state=QuestStates.naming)
    dp.register_message_handler(quest_proc, state=QuestStates.session)
    dp.register_message_handler(warning)