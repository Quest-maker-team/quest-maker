"""client

Client commands handler file.
"""

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
from keyboards import *

from db.db import *


class Tip:
    """The type corresponding to the hint.
    """
    def __init__(self, id, fine, msg):
        """Constructor.
        :param self: instance
        :param id: hint id
        :param fine: fine for a hint
        :param msg: hint message
        """
        self.id = id
        self.fine = fine
        self.msg = msg
        self.files = []


    def load_files(self):
        """Load tip files.
        :param self: instance
        """
        res = get_hint_files(self.id)
        if res != None:
            self.files = res


class QuestPoint:
    """Quest point representation type.
    """
    def __init__(self, id, type, msg):
        """Constructor.
        :param self: instance
        :param id: point id
        :param msg: point message
        """
        self.id = id
        self.type = type
        self.msg = msg
        self.next_points = None
        self.tips = []
        self.files = []


    def load_next_points(self):
        """Load next points.
        :param self: instance
        """
        points_info = get_answer_options(self.id)
        if points_info is None:
            return
        if len(points_info) == 0:
            return

        self.next_points = {}
        for i in range(len(points_info)):
            if points_info[i][2] is None:
                point = None
            else:
                question_info = get_question_by_id(points_info[i][2])
                point = QuestPoint(question_info[0], question_info[2], question_info[1])
            self.next_points[points_info[i][0]] = (points_info[i][1], point)


    def load_tips(self):
        """Load point tips.
        :param self: instance
        """
        res = get_hints(self.id)
        if res != None:
            for r in res:
                tip = Tip(r[0], r[1], r[2])
                tip.load_files()
                self.tips.append(tip)


    def load_files(self):
        """Load point files.
        :param self: instance
        """
        res = get_question_files(self.id)
        if res != None:
            self.files = res


    def get_tip(self):
        """Get point tips.
        :param self: instance
        :return instance of the Tip class
        :return None if there is no more tip
        """
        if len(self.tips) == 0:
            return None
        res = self.tips[0]
        del self.tips[0]
        return res


    def get_next(self, point_name):
        """Get next point.
        :param self: instance
        :param point_name: answer for next point
        :return score to add and next point if success
        :return None if there is no such answer
        """
        if self.type == "open" or self.type == "choice":
            if point_name in self.next_points:
                point_info = self.next_points[point_name]
                if point_info[1] is None:
                    return (point_info[0], None)
                else:
                    point_info[1].load_next_points()
                    point_info[1].load_tips()
                    point_info[1].load_files()
                    return (point_info[0], point_info[1])
            return (0, None)
        # movement
        point_info = list(self.next_points.items())[0][1]
        point_info[1].load_next_points()
        point_info[1].load_tips()
        point_info[1].load_files()
        return (point_info[0], point_info[1])


def get_quest_info(quest_id):
    """Get quest info.
    :param quest_id: quest id
    :return first point
    """
    first_point_info = get_first_question(quest_id)
    first_point = QuestPoint(first_point_info[0], first_point_info[2], first_point_info[1])

    first_point.load_next_points()
    first_point.load_tips()
    first_point.load_files()

    return first_point


class Quest:
    """Quest representation type.
    """
    def __init__(self, quest_id):
        """Constructor.
        :param self: instance
        :param quest_id: quest id
        """
        self.quest_id = quest_id
        self.score = 0
        self.cur_point = get_quest_info(quest_id)


    def next_point(self, message):
        """Go to next point.
        :param self: instance
        :param name: message from user
        :return (False, <message to send>, <list of files>) if quest need continue
        :return (True, <message to send>, <list of files>) if quest is over
        """
        (score_to_add, point) = self.cur_point.get_next(message)
        self.score += score_to_add
        if point is None:
            return (False, "Неправильный ответ.", [])
        self.cur_point = point
        if point.next_points is None:
            return (True, point.msg, point.files)
        return (False, point.msg, point.files)


class QuestStates(StatesGroup):
    """Quest states for aiogram state machine.
    """
    naming = State()
    session = State()


async def cmd_start(message: types.Message):
    """Command start handler.
    :param message: message from user
    """
    await message.answer('Это бот для игры в квесты, созданные при помощи сервиса QuestCreator.',
        reply_markup=ReplyKeyboardRemove())


def activate_quest(quest_id):
    """Check if quest exists.
    :param quest_id: quest id
    """
    return get_quest_title(quest_id) != None


async def cmd_quest(message: types.Message):
    """Command start quest handler.
    :param message: message from user
    """
    await QuestStates.naming.set()
    await message.answer('Введите идентификатор квеста.')


def add_file_to_media(media: types.MediaGroup, file, caption):
    """Add file to the media group
    :param media: media group
    :param file: tuple with values url and type name
    :param caption: caption to file
    """
    if file[1] == 'image':
        media.attach_photo(file[0], caption=caption)
    elif file[1] == 'audio':
        media.attach_audio(file[0], caption=caption)
    elif file[1] == 'video':
        media.attach_video(file[0], caption=caption)


async def send_files(message: types.Message, caption, files, reply_markup):
    """Send files with caption to the chat
    :param message: message from user
    :param caption: caption
    :param files: list of tuples with values url and type name
    """
    if len(files) == 0:
        if caption != '':
            await message.answer(caption, reply_markup=reply_markup)
    else:
        await types.ChatActions.upload_document()
        media = types.MediaGroup()
        for i in range(len(files)):
            add_file_to_media(media, files[i], '')
        await message.answer_media_group(media)
        if caption != '':
            await message.answer(caption, reply_markup=reply_markup)
        else:
            #if only a file, but you need to change the keyboard (it won't send an empty line)
            await message.answer('↑', reply_markup=reply_markup)

async def name_quest(message: types.Message, state: FSMContext):
    """Naming quest state handler.
    :param message: message from user
    :param state: state machine context
    """
    if activate_quest(message.text):
        async with state.proxy() as data:
            data['quest'] = Quest(message.text)
        await QuestStates.next()
        await message.answer('Квест "' + get_quest_title(message.text) + '" начат. '
            'Чтобы закончить напишите /end, '
            'чтобы получить количество баллов - /score, '
            'чтобы получить подсказку - /tip, '
            'чтобы попытаться пропустить точку - /skip.')
        await send_files(message, data['quest'].cur_point.msg, data['quest'].cur_point.files, ReplyKeyboardRemove())
    else:
        await message.reply('Квест с идентификатором "' + message.text + '" не найден',
            reply_markup=ReplyKeyboardRemove())
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


async def tip_handler(message: types.Message, state: FSMContext):
    """Get tip handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        if 'quest' in data:
            tip = data['quest'].cur_point.get_tip()
            if tip is None:
                await message.reply('Больше подсказок нет.',
                    reply_markup=ReplyKeyboardRemove())
            else:
                await send_files(message, tip.msg, tip.files, ReplyKeyboardRemove())
                await message.answer('Штраф за подсказку: ' + str(tip.fine) + ' баллов.')
                data['quest'].score -= tip.fine
        else:
            await message.answer('Выберите квест командой /quest.', reply_markup=ReplyKeyboardRemove())


async def score_handler(message: types.Message, state: FSMContext):
    """Get score handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        if 'quest' in data:
            await message.reply('Текущее количество баллов: ' + str(data['quest'].score) + '.',
                reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer('Выберите квест командой /quest.', reply_markup=ReplyKeyboardRemove())


async def skip_handler(message: types.Message, state: FSMContext):
    """Skip pointer handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        if 'quest' in data:
            if 'skip' in data['quest'].cur_point.next_points:
                (quest_ends, msg, files) = data['quest'].next_point('skip')
                if data['quest'].cur_point.type == "open":
                    await send_files(message, msg, files, ReplyKeyboardRemove())
                elif data['quest'].cur_point.type == "choice":
                    keyboard = create_keyboard(data['quest'].cur_point.next_points)
                    await send_files(message, msg, files, keyboard)
            else:
                await message.answer('Точка не поддерживает пропуск.')
        else:
            await message.answer('Выберите квест командой /quest.', reply_markup=ReplyKeyboardRemove())


async def quest_proc(message: types.Message, state: FSMContext):
    """Quest processing handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        (quest_ends, msg, files) = data['quest'].next_point(message.text)
        if data['quest'].cur_point.type == "open":
            await send_files(message, msg, files, ReplyKeyboardRemove())
        elif data['quest'].cur_point.type == "choice":
            keyboard = create_keyboard(data['quest'].cur_point.next_points)
            await send_files(message, msg, files, keyboard)
        else: # movement
            await send_files(message, msg, files, ReplyKeyboardRemove())
        if quest_ends == True:
            await state.finish()
            await message.answer('Квест "' + get_quest_title(data['quest'].quest_id) + '" закончен. '
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
    dp.register_message_handler(tip_handler, state='*', commands="tip")
    dp.register_message_handler(skip_handler, state='*', commands="skip")
    dp.register_message_handler(name_quest, state=QuestStates.naming)
    dp.register_message_handler(quest_proc, state=QuestStates.session)
    dp.register_message_handler(warning)