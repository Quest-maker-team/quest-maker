"""client

Client commands handler file.
"""

from ast import keyword
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
import re


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
    now = datetime.datetime.now().timetz()
    open = True
    not_close = True

    if open_time != None:
        open = now > open_time.timetz()
    if close_time != None:
        not_close = now < close_time.timetz()
    if open_time != None and close_time != None:
        # 22:00 - 2:00, for example
        if open_time.timetz() > close_time.timetz():
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
        if time_limits[1] < datetime.datetime.now().astimezone() - time_start:
            return False

    if time_limits[0] != None:
        if datetime.datetime.now().astimezone() > time_limits[0]:
            return False

    return True


class QuestPoint:
    """message when user don't want to locate 'em"""
    no_geo_msg = "Я на месте, геоданных не дам"

    """Quest point representation type.
    """
    def __init__(self, id, type, msg, next_id):
        """Constructor.
        :param self: instance
        :param id: point id
        :param msg: point message
        :param next_id: next point id
        """
        self.id = id
        self.type = type
        self.msg = msg
        self.next_point_id = next_id
        self.next_points = None
        self.tips = []
        self.files = []


    def load_next_points(self):
        """Load next points.
        :param self: instance
        """
        if self.type == 'open_question' or self.type == 'choice_question':
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
                        block_info = get_block_by_id(points_info[i][2])
                        point = QuestPoint(block_info[0], block_info[2], block_info[1], block_info[3])
                    if 'open_question' == self.type:
                        points_info[i][0] = points_info[i][0].lower()
                    self.next_points[points_info[i][0]] = (points_info[i][1], point)
            except:
                self.next_points = None
        else:
            try:
                if self.next_point_id is not None:
                    block_info = get_block_by_id(self.next_point_id)
                    self.next_points = QuestPoint(block_info[0], block_info[2], block_info[1], block_info[3])
            except:
                pass


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
        res = get_block_files(self.id)
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


    def get_next(self, point_name=None, latitude=None, longitude=None):
        """Get next point.
        :param self: instance
        :param point_name: answer for next point
        :param latitude: geoposition latitude
        :param longitude: geoposition longitude
        :return score to add and next point if success
        :return None if there is no such answer
        :return (None, None) in case of movement failure
        """
        if self.type == 'open_question':
            point_name = point_name.lower()
        if self.type == 'open_question' or self.type == 'choice_question':
            name = ''
            if point_name in self.next_points:
                name = point_name
            elif '' in self.next_points: # universal wrong answer
                pass
            else:
                return (0, None)
            point_info = self.next_points[name]
            if point_info[1] is None:
                return (0, None)
            else:
                point_info[1].load_next_points()
                point_info[1].load_tips()
                point_info[1].load_files()
                return (point_info[0], point_info[1])
        elif self.type == 'movement':
            try:
                movement_info = get_place(self.id)
                if latitude is not None and longitude is not None:
                    dist = geopy.distance.geodesic((float(movement_info[0]), float(movement_info[1])), (latitude, longitude)).m
                    if dist > movement_info[2]:
                        return (0, None)
                elif point_name != QuestPoint.no_geo_msg:
                    return (0, None)
                if not check_time(movement_info[3], movement_info[4]):
                    return (0, None)
            except:
                return (None, None)
        if self.next_points is not None:
            self.next_points.load_next_points()
            self.next_points.load_tips()
            self.next_points.load_files()
            return (0, self.next_points)
        else:
            return (0, None)
        

def get_quest_info(quest_id):
    """Get quest info.
    :param quest_id: quest keyword
    :return quest id, first point and title
    :return (None, None, '') in case of failure
    """
    id, name = get_quest_title(quest_id)
    first_point_info = get_start_block(id)
    # here name can be None when, for example, the time of the quest activity came out
    if first_point_info is None or name is None:
        return (None, None, '')

    first_point = QuestPoint(first_point_info[0], 'start_block', first_point_info[2], first_point_info[1])

    first_point.load_next_points()
    first_point.load_files()

    return id, first_point, name


class Quest:
    """Quest representation type.
    """
    def __init__(self, quest_id):
        """Constructor.
        :param self: instance
        :param quest_id: quest keyword
        """
        self.score = 0
        self.quest_id, self.cur_point, self.name = get_quest_info(quest_id)
        self.time_limits = get_quest_time_info(self.quest_id)
        self.time_start = datetime.datetime.now().astimezone()
        self.complition_time = datetime.timedelta()


    def save(self, telegram_id, is_finished):
        """Save the state of the quest in the history
        :param self: instance
        :param telegram_id: user id
        :param is_finished: quest status, is true if it is completed to the end
        """
        last_block_id = None
        if not is_finished:
            if self.time_limits[1] is None:
                last_block_id = self.cur_point.id
        self.complition_time += datetime.datetime.now().astimezone() - self.time_start
        save_history(self.quest_id, telegram_id, is_finished, last_block_id, self.score, self.time_start, self.complition_time)


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
        
        point_info = get_block_by_id(info[1])
        if point_info is None:
            return False

        point = QuestPoint(point_info[0], point_info[2], point_info[1], point_info[3])
        point.load_next_points()
        point.load_tips()
        point.load_files()
        self.cur_point = point
        self.score = info[2]
        self.complition_time = info[3]

        return True


    def next_point(self, message=None, latitude=None, longitude=None):
        """Go to next point.
        :param self: instance
        :param message: message from user
        :param latitude: geoposition latitude
        :param longitude: geoposition longitude
        :return (False, <message to send>, <list of files>, <point id>) if quest need continue
        :return (True, <message to send>, <list of files>, 0) if quest is over
        """
        if self.cur_point is None:
            return (True, "Ошибка в структуре квеста.", [], 0)

        if not check_time_limits(self.time_start, self.time_limits):
            return (False, "Время активности квеста закончилось.", [], 0)

        (score_to_add, point) = self.cur_point.get_next(message, latitude, longitude)
        if self.cur_point.type == 'movement' and point is None:
            if score_to_add != None:
                return (False, "Неверное место или время.", [], 0)
            else:
                return (True, "Ошибка в структуре квеста.", [], 0)
        self.score += score_to_add
        if point is None:
            return (True, "Ошибка в структуре квеста.", [], 0)
        
        if point.type == 'end_block':
            return (True, point.msg, point.files, 0)
        elif point.next_points is None:
            return (True, "Ошибка в структуре квеста.", [], 0)
        
        self.cur_point = point
        return (False, point.msg, point.files, point.id)


class QuestStates(StatesGroup):
    """Quest states for aiogram state machine.
    """
    naming = State()
    password = State()
    loading = State()
    session = State()
    rating = State()


async def cmd_start(message: types.Message):
    """Command start handler.
    :param message: message from user
    """
    await set_commands(bot)
    await message.answer('Это бот для игры в квесты, созданные при помощи сервиса QuestCreator. '
        'Введите команду /quest для начала.',
        reply_markup=create_opening_menu_keyboard())


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
    await message.answer('Введите идентификатор квеста.', reply_markup=ReplyKeyboardRemove())


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
            media.attach_photo(types.InputFile(i[0]))
        for v in video:
            media.attach_video(types.InputFile(v[0]))
        groups.append(media)

    if len(audio) != 0:
        media_a = types.MediaGroup()
        for a in audio:
            media_a.attach_audio(types.InputFile(a[0]))
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
            await message.answer('Ознакомьтесь с медиа данными', reply_markup=reply_markup)


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
    quest_info = get_private_quest_title(message.text)
    if quest_info:
        async with state.proxy() as data:
            data['keyword'] = message.text
            data['quest-name'] = quest_info[1]
        await message.answer('Квест ' + quest_info[1] + ' приватный. Введите пароль.')
        await QuestStates.password.set()
        return

    quest_info = get_quest_title(message.text)
    if quest_info:
        async with state.proxy() as data:
            data['quest'] = Quest(message.text)
            if data['quest'].cur_point is None:
                await message.answer('Не удалось запустить квест.')
                await state.finish()
                return
            info = get_history(quest_info[0], message.from_user.id)
            if info is None:
                pass
            elif info[0] or (info[1] is None):
                pass
            else:
                await QuestStates.loading.set()
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

            keyboard = ReplyKeyboardRemove()
            await send_files(message, data['quest'].cur_point.msg, data['quest'].cur_point.files, keyboard)
    else:
        await message.reply('Квест с идентификатором "' + message.text + '" не найден',
            reply_markup=create_opening_menu_keyboard())
        await state.finish()


async def password_quest(message: types.Message, state: FSMContext):
    """Insert password of private quest state handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        quest_name = data['quest-name']
        keyword = data['keyword']
    quest_info = get_private_quest_title(keyword)
    if quest_info:
        if quest_info[2] != message.text:
            await message.reply('Неправильный пароль к квесту "' + quest_name + '".',
                reply_markup=create_opening_menu_keyboard())
            await state.finish()
            return
        async with state.proxy() as data:
            data['quest'] = Quest(keyword)
            if data['quest'].cur_point is None:
                await message.answer('Не удалось запустить квест.')
                await state.finish()
                return
            info = get_history(quest_info[0], message.from_user.id)
            if info is None:
                pass
            elif info[0] or (info[1] is None):
                pass
            else:
                await QuestStates.loading.set()
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
            
            keyboard = ReplyKeyboardRemove()
            await send_files(message, data['quest'].cur_point.msg, data['quest'].cur_point.files, keyboard)
    else:
        await message.reply('Квест с идентификатором "' + quest_name + '" не найден',
            reply_markup=create_opening_menu_keyboard())
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

            keyboard = ReplyKeyboardRemove()
            await send_files(message, data['quest'].cur_point.msg, data['quest'].cur_point.files, keyboard)
        else:
            if data['quest'].load(message.from_user.id):
                await QuestStates.next()
                if data['quest'].cur_point.type == "movement":
                    await send_files(message, data['quest'].cur_point.msg, data['quest'].cur_point.files, create_movement_keyboard(QuestPoint.no_geo_msg))
                    movement_info = get_place(data['quest'].cur_point.id)
                    await bot.send_location(message.chat.id, movement_info[0], movement_info[1])
                else:
                    if data['quest'].cur_point.type == "choice_question":
                        keyboard = create_keyboard(edit_options(data['quest'].cur_point.next_points))
                    elif data['quest'].cur_point.type == "message":
                        keyboard = create_keyboard(['Дальше'])
                    else:
                        keyboard = ReplyKeyboardRemove()
                    await send_files(message, data['quest'].cur_point.msg, data['quest'].cur_point.files, keyboard)
            else:
                await message.answer('Не удалось возобновить прохождение.',
                    reply_markup=create_opening_menu_keyboard())
                await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    """Cancel session handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        if 'quest' in data:
            data['quest'].save(message.from_user.id, False)
            await message.answer('Квест "' + data['quest'].name + '" остановлен. '
                                 'Количество баллов: ' + str(data['quest'].score) + ".",
                                 reply_markup=create_opening_menu_keyboard())
        else:
            await message.answer('Выберите квест командой /quest.', reply_markup=create_opening_menu_keyboard())
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
            await message.answer('Выберите квест командой /quest.', reply_markup=create_opening_menu_keyboard())


async def score_handler(message: types.Message, state: FSMContext):
    """Get score handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        if 'quest' in data:
            await message.reply('Текущее количество баллов: ' + str(data['quest'].score) + '.')
        else:
            await message.answer('Выберите квест командой /quest.', reply_markup=create_opening_menu_keyboard())


async def skip_handler(message: types.Message, state: FSMContext):
    """Skip pointer handler.
    :param message: message from user
    :param state: state machine context
    """
    async with state.proxy() as data:
        if 'quest' in data:
            if data['quest'].cur_point.type == "open_question" or data['quest'].cur_point.type == "choice_question":
                if 'skip' in data['quest'].cur_point.next_points:
                    score = data['quest'].score
                    (quest_ends, msg, files, id) = data['quest'].next_point('skip')
                    score_delta = data['quest'].score - score
                    if score_delta > 0:
                        await message.answer('Получены баллы: ' + str(score_delta) + '. ')
                    elif score_delta < 0:
                        await message.answer('Отняты баллы: ' + str(-score_delta) + '. ')
                    if data['quest'].cur_point.type == "choice_question":
                        keyboard = create_keyboard(edit_options(data['quest'].cur_point.next_points))
                        await send_files(message, msg, files, keyboard)
                    else:
                        await send_files(message, msg, files, ReplyKeyboardRemove())
                    if quest_ends == True:
                        data['quest'].save(message.from_user.id, True)
                        await message.answer('Квест "' + data['quest'].name + '" закончен. '
                                             'Количество баллов: ' + str(data['quest'].score) + ".",
                                              reply_markup=create_rating_keyboard())
                        await QuestStates.rating.set()
                else:
                    await message.answer('Точка не поддерживает пропуск.')
            else:
                await message.answer('Точка не поддерживает пропуск.')
        else:
            await message.answer('Выберите квест командой /quest.', reply_markup=create_opening_menu_keyboard())


async def point_proc(message: types.Message, state: FSMContext, latitude, longitude):
    """Quest point processing.
    :param message: message from user
    :param state: state machine context
    :param latitude: geoposition latitude
    :param longitude: geoposition longitude
    """
    async with state.proxy() as data:
        score = data['quest'].score
        (quest_ends, msg, files, id) = data['quest'].next_point(message.text, latitude=latitude, longitude=longitude)
        score_delta = data['quest'].score - score
        if score_delta > 0:
            await message.answer('Получены баллы: ' + str(score_delta) + '. ')
        elif score_delta < 0:
            await message.answer('Отняты баллы: ' + str(-score_delta) + '. ')
        if data['quest'].cur_point.type == "choice_question":
            keyboard = create_keyboard(edit_options(data['quest'].cur_point.next_points))
            await send_files(message, msg, files, keyboard)
        elif data['quest'].cur_point.type == "message":
            keyboard = create_keyboard(['Дальше'])
            await send_files(message, msg, files, keyboard)
        elif data['quest'].cur_point.type == "movement":
            await send_files(message, msg, files, create_movement_keyboard(QuestPoint.no_geo_msg))
            movement_info = get_place(data['quest'].cur_point.id)
            await bot.send_location(message.chat.id, movement_info[0], movement_info[1])
        else:
            await send_files(message, msg, files, ReplyKeyboardRemove())
        if quest_ends == True:
            if msg == 'Ошибка в структуре квеста.' or msg == 'Время активности квеста закончилось.':
                data['quest'].save(message.from_user.id, False)
            else:
                data['quest'].save(message.from_user.id, True)
            await message.answer('Квест "' + data['quest'].name + '" закончен. '
                                 'Количество баллов: ' + str(data['quest'].score) + ".",
                                  reply_markup=create_rating_keyboard())
            await QuestStates.rating.set()


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
    await message.answer('Выберите квест командой /quest.', reply_markup=create_opening_menu_keyboard())


async def handle_location(message: types.Message, state: FSMContext):
    """Location processing handler.
    :param message: message from user
    :param state: state machine context
    """
    lat = message.location.latitude
    lon = message.location.longitude
    await point_proc(message, state, lat, lon)


async def cmd_help(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'quest' in data:
            await message.answer('Квест "' + data['quest'].name + '" уже запущен. '
                                 'Чтобы закончить напишите /end, '
                                 'чтобы получить количество баллов - /score, '
                                 'чтобы получить подсказку - /tip, '
                                 'чтобы попытаться пропустить точку - /skip.')
        else:
            await message.answer('Выберите квест командой /quest.')


async def rate_quest(message: types.Message, state: FSMContext):
    """Rating quest state handler.
    :param message: message from user
    :param state: state machine context
    """
    rating = get_rating(message.text)
    if rating is None:
        await message.reply('Неправильная оценка. Воспользуйтесь клавиатурой.')
    async with state.proxy() as data:
        update_rating(data['quest'].cur_point.id, rating)
        await message.answer('Спасибо за отзыв.', reply_markup=create_opening_menu_keyboard())
    await state.finish()


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
    dp.register_message_handler(cmd_help, state='*', commands="help")
    dp.register_message_handler(name_quest, state=QuestStates.naming)
    dp.register_message_handler(password_quest, state=QuestStates.password)
    dp.register_message_handler(load_quest, state=QuestStates.loading)
    dp.register_message_handler(quest_proc, state=QuestStates.session)
    dp.register_message_handler(rate_quest, state=QuestStates.rating)
    dp.register_message_handler(warning)
    dp.register_message_handler(handle_location, content_types=['location'], state=QuestStates.session)
