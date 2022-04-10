"""client

Client commands handler file.
"""

import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardRemove
from keyboards import *

from create_bot import bot
from db.db import *
from handlers.commands import *

import geopy.distance


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


def check_time(open_time, close_time):
    """Checks whether the current time is in the specified interval
    :param open_time: the beginning of time interval
    :param close_time: end of time interval
    :return True if we are in the specified interval
    :return False otherwise
    """
    now = datetime.datetime.now().time()
    open = True
    not_close = True

    if open_time != None:
        open = now > open_time.time()
    if close_time != None:
        not_close = now < close_time.time()
    if open_time != None and close_time != None:
        # 22:00 - 2:00, for example
        if open_time.time() > close_time.time():
            return open or not_close
        else:
            return open and not_close
    else:
        return open and not_close


def check_time_limits(time_start, time_limits):
    """Checks whether we are keeping within the time limits
    :param time_start: the start time of the quest
    :param time_limits: a tuple with the closing time of the quest and a time limit on the passage
    :return True if we are keeping within the time limits
    :return False otherwise
    """
    if time_limits is None:
        return True
    
    if time_limits[1] != None:
        if time_limits[1] < datetime.datetime.now() - time_start:
            return False

    if time_limits[0] != None:
        if datetime.datetime.now() > time_limits[0]:
            return False

    return True


class QuestPoint:
    """message when user don't want to locate 'em"""
    no_geo_msg = "Я не хочу раскрывать своё положение, но добрался до места"

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

        try:
            self.next_points = {}
            for i in range(len(points_info)):
                if points_info[i][2] is None:
                    point = None
                else:
                    question_info = get_question_by_id(points_info[i][2])
                    point = QuestPoint(question_info[0], question_info[2], question_info[1])
                self.next_points[points_info[i][0]] = (points_info[i][1], point)
        except:
            #delete all the options, because for example, an error when loading the correct answer will
            #greatly distort the meaning
            self.next_points = None


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


    def get_next(self, point_name, latitude=None, longitude=None):
        """Get next point.
        :param self: instance
        :param point_name: answer for next point
        :return score to add and next point if success
        :return None if there is no such answer
        :return (None, None) in case of movement failure
        """
        if self.type == "open" or self.type == "choice":
            name = ''
            if point_name in self.next_points:
                name = point_name
            elif '' in self.next_points: # universal wrong answer
                pass
            else:
                return (0, None)
            point_info = self.next_points[name]
            if point_info[1] is None:
                return (point_info[0], None)
            else:
                point_info[1].load_next_points()
                point_info[1].load_tips()
                point_info[1].load_files()
                return (point_info[0], point_info[1])
        # movement
        try:
            movement_info = get_movement(self.id)
            if latitude is not None and longitude is not None:
                dist = geopy.distance.geodesic(movement_info[1], (latitude, longitude)).m
                if dist > movement_info[2]:
                    return (None, None)
            elif point_name != QuestPoint.o_geo_msg:
                return None
            if not check_time(movement_info[3], movement_info[4]):
                return (0, None)
            question_info = get_question_by_id(movement_info[0])
            point = QuestPoint(question_info[0], question_info[2], question_info[1])
            point.load_next_points()
            point.load_tips()
            point.load_files()
            return (0, point)
        except:
            return (None, None)
        

def get_quest_info(quest_id):
    """Get quest info.
    :param quest_id: quest id
    :return start message, first point and title
    :return ('', None, '') in case of failure
    """
    name = get_quest_title(quest_id)
    start_msg, first_point_info = get_first_question(quest_id)
    # here name can be None when, for example, the time of the quest activity came out
    if first_point_info is None or name is None:
        return ('', None, '')

    first_point = QuestPoint(first_point_info[0], first_point_info[2], first_point_info[1])

    first_point.load_next_points()
    first_point.load_tips()
    first_point.load_files()

    # since it will not be possible to send an empty message
    if start_msg == '':
        start_msg += 'Доборо пожаловать на квест "' + name + '"'

    return start_msg, first_point, name


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
        self.start_msg, self.cur_point, self.name = get_quest_info(quest_id)
        self.time_limits = get_quest_time_info(quest_id)
        self.time_start = datetime.datetime.now()


    def save(self, telegram_id, is_finished):
        """Save the state of the quest in the history
        :param self: instance
        :param telegram_id: user id
        :param is_finished: quest status, is true if it is completed to the end
        """
        last_question_id = None
        if not is_finished:
            if self.time_limits[1] is None:
                if datetime.datetime.now() < self.time_limits[0]:
                    last_question_id = self.cur_point.id
        save_history(self.quest_id, telegram_id, is_finished, last_question_id, self.score)


    def load(self, telegram_id):
        """Download the quest status from history
        :param self: instance
        :param telegram_id: user id
        :return True in case of success
        :return False in case of failure
        """
        info = get_history(self.quest_id, telegram_id)
        if info is None:
            return False
        if info[0] or (info[1] is None):
            return False
        
        point_info = get_question_by_id(info[1])
        if point_info is None:
            return False

        point = QuestPoint(point_info[0], point_info[2], point_info[1])
        point.load_next_points()
        point.load_tips()
        point.load_files()
        self.cur_point = point
        self.score = info[2]

        return True


    def next_point(self, message):
        """Go to next point.
        :param self: instance
        :param name: message from user
        :return (False, <message to send>, <list of files>) if quest need continue
        :return (True, <message to send>, <list of files>) if quest is over
        """
        if self.cur_point is None:
            return (True, "Ошибка в структуре квеста.", [])

        if not check_time_limits(self.time_start, self.time_limits):
            return (True, "Время активности квеста закончилось.", [])

        (score_to_add, point) = self.cur_point.get_next(message)
        if self.cur_point.type == 'movement' and point is None:
            if score_to_add != None:
                return (False, "Неверное место или время.", [])
            else:
                return (True, "Ошибка в структуре квеста.", [])
        self.score += score_to_add
        if point is None:
            return (False, "Неправильный ответ.", [])
        
        if point.type == 'end':
            return (True, point.msg, point.files)
        elif (point.type == 'open' or point.type == 'choice') and point.next_points is None:
            return (True, "Ошибка в структуре квеста.", [])
        
        self.cur_point = point
        return (False, point.msg, point.files)


class QuestStates(StatesGroup):
    """Quest states for aiogram state machine.
    """
    naming = State()
    loading = State()
    session = State()


async def cmd_start(message: types.Message):
    """Command start handler.
    :param message: message from user
    """
    await set_commands(bot)
    await message.answer('Это бот для игры в квесты, созданные при помощи сервиса QuestCreator.'
        'Введите команду /quest для начала.',
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


def make_media_groups(files):
    """Add file to the media group
    :param media: media group
    :param file: tuple with values url and type name
    :return list of media groups
    """
    image = []
    video = []
    audio = []
    groups = []
    for i in range(len(files)):
        if files[i][1] == 'image':
            image.append(files[i])
        elif files[i][1] == 'video':
            video.append(files[i])
        else:
            audio.append(files[i])

    if len(image) != 0 or len(video) != 0:
        media = types.MediaGroup()
        for i in image:
            media.attach_photo(i[0])
        for v in video:
            media.attach_video(v[0])
        groups.append(media)

    if len(audio) != 0:
        media_a = types.MediaGroup()
        for a in audio:
            media_a.attach_audio(a[0])
        groups.append(media_a)

    return groups


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
        try:
            await types.ChatActions.upload_document()
            groups = make_media_groups(files)
            for g in groups:
                await message.answer_media_group(g)
        except:
            await message.answer('Здесь должны были быть файлы, но загрузить их не удалось')

        if caption != '':
            await message.answer(caption, reply_markup=reply_markup)
        else:
            #if only a file, but you need to change the keyboard (it won't send an empty line)
            await message.answer('↑', reply_markup=reply_markup)


def edit_options(options):
    """Create a list of possible answers, excluding 'skip' and ''
    :param options: list of options
    :return new list of options without 'skip' and '' 
    """
    new_options = options.copy()
    if 'skip' in new_options:
        del new_options['skip']
    if '' in new_options:
        del new_options['']
    return new_options


async def name_quest(message: types.Message, state: FSMContext):
    """Naming quest state handler.
    :param message: message from user
    :param state: state machine context
    """
    if activate_quest(message.text):
        async with state.proxy() as data:
            data['quest'] = Quest(message.text)
            if data['quest'].cur_point is None:
                await message.answer('Не удалось запустить квест.')
                await state.finish()
                return
            
            info = get_history(message.text, message.from_user.id)
            if info is None:
                pass
            elif info[0] or (info[1] is None):
                pass
            else:
                await QuestStates.next()
                options = ['Да', 'Нет']
                keyboard = create_keyboard(options)
                await message.answer('Данный квест уже был начат Вами ранее. Желаете продолжить?',
                                     reply_markup=keyboard)
                return

            await QuestStates.session.set()
            await message.answer('Квест "' + data['quest'].name + '" начат. '
                'Чтобы закончить напишите /end, '
                'чтобы получить количество баллов - /score, '
                'чтобы получить подсказку - /tip, '
                'чтобы попытаться пропустить точку - /skip.')
            await message.answer(data['quest'].start_msg)

            if data['quest'].cur_point.type == "choice":
                keyboard = create_keyboard(edit_options(data['quest'].cur_point.next_points))
            else:
                keyboard = ReplyKeyboardRemove()
            await send_files(message, data['quest'].cur_point.msg, data['quest'].cur_point.files, keyboard)
            if data['quest'].cur_point.type == "end": # who knows if this will happen
                data['quest'].save(message.from_user.id, True)
                await message.answer('Квест "' + data['quest'].name + '" закончен. '
                                     'Количество баллов: ' + str(data['quest'].score) + ".",
                                     reply_markup=ReplyKeyboardRemove())
                await state.finish()
    else:
        await message.reply('Квест с идентификатором "' + message.text + '" не найден',
            reply_markup=ReplyKeyboardRemove())
        await state.finish()


async def load_quest(message: types.Message, state: FSMContext):
    """Loading quest state handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        if message.text == 'Нет':
            await QuestStates.session.set()
            await message.answer('Квест "' + data['quest'].name + '" начат. '
                    'Чтобы закончить напишите /end, '
                    'чтобы получить количество баллов - /score, '
                    'чтобы получить подсказку - /tip, '
                    'чтобы попытаться пропустить точку - /skip.')
            await message.answer(data['quest'].start_msg)

            if data['quest'].cur_point.type == "choice":
                keyboard = create_keyboard(edit_options(data['quest'].cur_point.next_points))
            else:
                keyboard = ReplyKeyboardRemove()
            await send_files(message, data['quest'].cur_point.msg, data['quest'].cur_point.files, keyboard)
            if data['quest'].cur_point.type == "end": # who knows if this will happen
                data['quest'].save(message.from_user.id, True)
                await message.answer('Квест "' + data['quest'].name + '" закончен. '
                                     'Количество баллов: ' + str(data['quest'].score) + ".",
                                     reply_markup=ReplyKeyboardRemove())
                await state.finish()
        else:
            if data['quest'].load(message.from_user.id):
                await QuestStates.next()
                if data['quest'].cur_point.type == "choice":
                    keyboard = create_keyboard(edit_options(data['quest'].cur_point.next_points))
                else:
                    keyboard = ReplyKeyboardRemove()
                await send_files(message, data['quest'].cur_point.msg, data['quest'].cur_point.files, keyboard)
            else:
                await message.answer('Не удалось возобновить прохождение.')
                await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    """Cancel session handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        if 'quest' in data:
            data['quest'].save(message.from_user.id, False)
            await message.answer('Квест "' + data['quest'].name + '" закончен. '
                                 'Количество баллов: ' + str(data['quest'].score) + ".",
                                 reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer('Выберите квест командой /quest.', reply_markup=ReplyKeyboardRemove())
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
                await message.answer('Штраф за подсказку в баллах: ' + str(tip.fine) + ' .')
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
            if data['quest'].cur_point.type == "open" or data['quest'].cur_point.type == "choice":
                if 'skip' in data['quest'].cur_point.next_points:
                    (quest_ends, msg, files) = data['quest'].next_point('skip')
                    if data['quest'].cur_point.type == "choice":
                        keyboard = create_keyboard(edit_options(data['quest'].cur_point.next_points))
                        await send_files(message, msg, files, keyboard)
                    else:
                        await send_files(message, msg, files, ReplyKeyboardRemove())
                    if quest_ends == True:
                        data['quest'].save(message.from_user.id, True)
                        await state.finish()
                        await message.answer('Квест "' + data['quest'].name + '" закончен. '
                                             'Количество баллов: ' + str(data['quest'].score) + ".",
                                              reply_markup=ReplyKeyboardRemove())
                else:
                    await message.answer('Точка не поддерживает пропуск.')
            else:
                await message.answer('Точка не поддерживает пропуск.')
        else:
            await message.answer('Выберите квест командой /quest.', reply_markup=ReplyKeyboardRemove())


async def point_proc(message: types.Message, state: FSMContext, latitude, longitude):
    async with state.proxy() as data:
        (quest_ends, msg, files) = data['quest'].next_point(message.text, latitude=latitude, longitude=longitude)
        if data['quest'].cur_point.type == "choice":
            keyboard = create_keyboard(edit_options(data['quest'].cur_point.next_points))
            await send_files(message, msg, files, keyboard)
        elif data['quest'].cur_point.type == "movement":
            await send_files(message, msg, files, create_movement_keyboard(QuestPoint.no_geo_msg))
        else:
            await send_files(message, msg, files, ReplyKeyboardRemove())
        if quest_ends == True:
            if msg == 'Ошибка в структуре квеста.' or msg == 'Время активности квеста закончилось.':
                data['quest'].save(message.from_user.id, False)
            else:
                data['quest'].save(message.from_user.id, True)
            await state.finish()
            await message.answer('Квест "' + data['quest'].name + '" закончен. '
                                 'Количество баллов: ' + str(data['quest'].score) + ".",
                                  reply_markup=ReplyKeyboardRemove())


async def quest_proc(message: types.Message, state: FSMContext):
    """Quest processing handler.
    :param message: message from user
    :param state: state machine context
    """
    await point_proc(message, state, None, None)


async def warning(message: types.Message):
    """Warning message handler.
    :param message: message from user
    """
    await message.answer('Выберите квест командой /quest.')


async def handle_location(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    await point_proc(message, state, lat, lon)


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
    dp.register_message_handler(load_quest, state=QuestStates.loading)
    dp.register_message_handler(quest_proc, state=QuestStates.session)
    dp.register_message_handler(warning)
    dp.register_message_handler(handle_location, content_types=['location'], state=QuestStates.session)
