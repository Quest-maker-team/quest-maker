"""client

Client commands handler file.
"""

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestPoint:
    """Quest point representation type.
    """
    def __init__(self, msg):
        """Constructor.
        :param self: instance
        :param msg: point message
        """
        self.msg = msg
        self.next_points = None


    def load_next_points(self, points):
        """Load next points.
        :param self: instance
        :param msg: next points dictionary
        """
        self.next_points = points


    def get_next(self, point_name):
        """Get next point.
        :param self: instance
        :param point_name: answer for next point
        :return score to add and next point if success
        :return None if there is no such answer
        """
        if point_name in self.next_points:
            return self.next_points[point_name]
        return None


def get_quest_info(name):
    """Get quest info.
    :param name: quest name
    :return start message, first point and end message tuple
    """
    start_msg = 'Привет. Это нулевой квест проекта QuestMaker.'
    end_msg = 'До свидания от нулевого квеста.'
    
    point_cormen = QuestPoint("Осуждаем.")
    point_dijkstra = QuestPoint("Одобряем.")
    point_novikov = QuestPoint("Гиперодобряем.")

    point_dm_question = QuestPoint("Ваш любимый исследователь дискретной математики из "
        "Эдсрега А. Дейкстры, Томаса Г. Кормена и Фёдора А. Новикова?")
    point_dm_question.load_next_points(
        {'Кормен': (-5, point_cormen), 'Дейкстра': (5, point_dijkstra), 'Новиков': (10, point_novikov)})

    point_arithmetic = QuestPoint("2+2?")
    point_arithmetic.load_next_points({"4": (1, point_dm_question)})

    return (start_msg, point_arithmetic, end_msg)


class Quest:
    """Quest representation type.
    """
    def __init__(self, name):
        """Constructor.
        :param self: instance
        :param name: quest name
        """
        self.name = name
        self.score = 0
        (self.start_msg, self.cur_point, self.end_msg) = get_quest_info(name)


    def next_point(self, message):
        """Go to next point.
        :param self: instance
        :param name: message from user
        :return (False, <message to send>) if quest need continue
        :return (True, <message to send>) if quest is over
        """
        (score_to_add, point) = self.cur_point.get_next(message)
        self.score += score_to_add
        if point is None:
            return (False, "Неправильный ответ.")
        self.cur_point = point
        if point.next_points is None:
            return (True, point.msg)
        return (False, point.msg)


class QuestStates(StatesGroup):
    """Quest states for aiogram state machine.
    """
    naming = State()
    session = State()


async def cmd_start(message: types.Message):
    """Command start handler.
    :param message: message from user
    """
    await message.answer('Это бот для игры в квесты, созданные при помощи сервиса QuestCreator.')


def activate_quest(name):
    """Check if quest exists.
    :param name: quest name
    """
    return name == "zero"


async def cmd_quest(message: types.Message):
    """Command start quest handler.
    :param message: message from user
    """
    await QuestStates.naming.set()
    await message.answer('Введите имя квеста.')


async def name_quest(message: types.Message, state: FSMContext):
    """Naming quest state handler.
    :param message: message from user
    :param state: state machine context
    """
    if activate_quest(message.text):
        async with state.proxy() as data:
            data['quest'] = Quest(message.text)
        await QuestStates.next()
        await message.answer('Квест "' + message.text + '" начат. '
            'Чтобы закончить напишите /end, '
            'чтобы получить количество баллов - /score.')
        await message.answer(data['quest'].cur_point.msg)
    else:
        await message.reply('Квест "' + message.text + '" не найден')
        await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    """Cancel session handler.
    :param message: message from user
    :param state: state machine context
    """
    currentState = await state.get_state()
    if currentState is None:
        return
    await state.finish()


async def score_handler(message: types.Message, state: FSMContext):
    """Get score handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        if 'quest' in data:
            await message.reply('Текущее количество баллов: ' + str(data['quest'].score) + '.')
        else:
            await message.answer('Выберите квест командой /quest.')


async def quest_proc(message: types.Message, state: FSMContext):
    """Quest processing handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        (quest_ends, msg) = data['quest'].next_point(message.text)
        await message.answer(msg)
        if quest_ends == True:
            await message.answer(data['quest'].end_msg)
            await state.finish()
            await message.answer('Квест "' + data['quest'].name + '" закончен. '
                'Количество баллов: ' + str(data['quest'].score) + ".")


async def warning(message: types.Message):
    """Warning message handler.
    :param message: message from user
    """
    await message.answer('Выберите квест командой /quest.')


def register_client_handlers(dp: Dispatcher):
    """Register message handlers.
    :param dp: dispatcher
    """
    dp.register_message_handler(cmd_start, commands=['start', 'help'])
    dp.register_message_handler(cmd_quest, commands='quest')
    dp.register_message_handler(cancel_handler, state='*', commands="end")
    dp.register_message_handler(score_handler, state='*', commands="score")
    dp.register_message_handler(name_quest, state=QuestStates.naming)
    dp.register_message_handler(quest_proc, state=QuestStates.session)
    dp.register_message_handler(warning)