from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import date
import logging

from loader import dp, bot
from db import Users
from settings import LOG_FILE
from filters import IsUserPersonal
from message import MESSAGE
from user_features import interval_charts, long_charts


logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    filemode='a',
                    datefmt='%Y-%m-%d, %H:%M',
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')
log = logging.getLogger('Bot')


digital_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
digital_keyboard.row('1', '2', '3')
digital_keyboard.row('4', '5', '6')
digital_keyboard.row('7', '8', '9')
digital_keyboard.row(' ', '0', ' ')
digital_keyboard.row('Назад')

finish_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
finish_keyboard.row('Интервальная', 'Длительная')
finish_keyboard.row('Назад')


class Pace(StatesGroup):
    """
    Enter digits for 1km pace
    format, example:
    3:45 min/km is:
    minutes = 3
    dec_seconds = 4
    seconds = 5
    total-- is final state gives individual menu and handler
    interval-- state for /pace menu handler
    long-- state for /long menu handler
    """
    minutes = State()
    dec_seconds = State()
    seconds = State()
    total = State()
    interval = State()
    long = State()


@dp.message_handler(IsUserPersonal(), commands=['start'], state='*')
async def start(msg: types.Message, state: FSMContext):

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_name = msg.from_user.username
    today = date.today().strftime('%Y-%m-%d')
    info = (first_name, user_name, today)

    with Users() as users:
        users[user_id] = info

    await msg.reply(text=f'Привет, {first_name} 🙂 \n\n')
    await bot.send_message(user_id, text=MESSAGE['start'])

    log.info(f'{first_name} push /start button.')


@dp.message_handler(IsUserPersonal(), commands=['pace'], state='*')
async def pace(msg: types.Message, state: FSMContext):

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_name = msg.from_user.username
    today = date.today().strftime('%Y-%m-%d')
    info = (first_name, user_name, today)

    # new user to db or update user info: username and login date
    with Users() as users:
        users[user_id] = info

    await state.finish()
    await state.update_data(interval=True)
    await state.update_data(long=None)
    await Pace.first()
    await bot.send_message(user_id, text=MESSAGE['pace'], reply_markup=digital_keyboard)

    log.info(f'{first_name} push /pace button.')


@dp.message_handler(IsUserPersonal(), commands=['long'], state='*')
async def long(msg: types.Message, state: FSMContext):

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_name = msg.from_user.username
    today = date.today().strftime('%Y-%m-%d')
    info = (first_name, user_name, today)

    # new user to db or update user info: username and login date
    with Users() as users:
        users[user_id] = info

    await state.finish()
    await state.update_data(long=True)
    await state.update_data(interval=None)
    await Pace.first()

    await bot.send_message(user_id, text=MESSAGE['pace'], reply_markup=digital_keyboard)

    log.info(f'{first_name} push /long button.')


@dp.message_handler(IsUserPersonal(), commands=['help'], state='*')
async def help_any_state(msg: types.Message, state: FSMContext):

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name

    await bot.send_message(user_id, text=MESSAGE['help'])
    log.info(f'{first_name} push /help button.')


@dp.message_handler(IsUserPersonal(), Text(equals='Интервальная'), state='*')
async def pace_form_total_interval_without_state(msg: types.Message, state: FSMContext):

    return await pace(msg=msg, state=state)


@dp.message_handler(IsUserPersonal(), Text(equals='Длительная'), state='*')
async def pace_form_total_long_without_state(msg: types.Message, state: FSMContext):

    return await long(msg=msg, state=state)


@dp.message_handler(IsUserPersonal(), Text(equals='Назад'), state='*')
async def cancel_pace_form(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
    # clear all enter digits state
    await state.finish()
    await message.reply(text=MESSAGE['cancel_pace_form'], reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda msg: msg.text.isdigit() and 0 < int(msg.text) < 2, state=Pace.minutes)
async def pace_form_invalid_minutes_0_or_1(msg: types.Message):
    """
    Exception: wrong enter minutes, Kipchoge style
    """
    return await msg.reply(text=MESSAGE['pace_form_invalid_minutes_0_or_1'])


@dp.message_handler(lambda msg: msg.text.isdigit() and 5 < int(msg.text) < 10, state=Pace.dec_seconds)
async def pace_form_invalid_dec_seconds_5_to_9(msg: types.Message):
    """
    Exception: wrong dec seconds, block enter 60- 90 seconds to form.
    """
    return await msg.reply(text=MESSAGE['pace_form_invalid_dec_seconds_6_to_9'])


@dp.message_handler(lambda msg: msg.text.isdigit() and 229 < int(msg.text) < 960, state=Pace.minutes)
async def pace_form_system_keyboard(msg: types.Message, state: FSMContext):
    """
    good conditions pace from system keyboard 2:30- 9:59 min/km.
    """

    user_id = msg.from_user.id
    pace = msg.text
    await msg.reply(text=f'Темп тренировки: {pace[0]}:{pace[1:]} мин/км.')
    minutes = pace[0]
    dec_seconds = pace[1]
    seconds = pace[2]
    pace1k = int(minutes) * 60 + int(dec_seconds) * 10 + int(seconds)
    async with state.proxy() as data:
        interval = data.get('interval')
        long = data.get('long')
    await state.finish()
    total = ''
    if interval:
        total = interval_charts(pace=pace1k)
    elif long:
        total = long_charts(pace=pace1k)
    await bot.send_message(user_id, text=total, reply_markup=finish_keyboard)


@dp.message_handler(lambda msg: not msg.text.isdigit()
                                and len(msg.text) == 4
                                and msg.text[1] in [':', ',', '.']
                                and msg.text[0].isdigit() and msg.text[2:].isdigit(),
                    state=Pace.minutes)
async def pace_form_system_keyboard_with_sep(msg: types.Message, state: FSMContext):
    """
    Обработка ввода с клавиатуры сразу 3 цифр с разделителем.
    """
    user_id = msg.from_user.id
    pace = msg.text

    await bot.send_message(user_id, text=f'Темп тренировки: {pace[0]}:{pace[2:]} мин/км.',
                           reply_markup=types.ReplyKeyboardRemove())
    minutes = pace[0]
    dec_seconds = pace[2]
    seconds = pace[3]
    pace1k = int(minutes) * 60 + int(dec_seconds) * 10 + int(seconds)
    async with state.proxy() as data:
        interval = data.get('interval')
        long = data.get('long')
    await state.finish()
    total = ''
    if interval:
        total = interval_charts(pace=pace1k)
    elif long:
        total = long_charts(pace=pace1k)
    await bot.send_message(user_id, text=total, reply_markup=finish_keyboard)


@dp.message_handler(lambda msg: msg.text.isdigit() and 1 < int(msg.text) < 10, state=Pace.minutes)
async def pace_form_first_digit(msg: types.Message, state: FSMContext):
    """
    Обработка первой цифры. Ввод минут, от 2мин до 9мин.
    """
    user_id = msg.from_user.id
    minutes = int(msg.text)

    await state.update_data(minutes=minutes)
    await Pace.next()
    await bot.send_message(user_id, text=f'Темп тренировки: {minutes}:xx мин/ км.', reply_markup=digital_keyboard)


@dp.message_handler(lambda msg: msg.text.isdigit() and int(msg.text) < 6, state=Pace.dec_seconds)
async def pace_form_second_digit(msg: types.Message, state: FSMContext):

    user_id = msg.from_user.id
    dec_seconds = int(msg.text)

    await state.update_data(dec_seconds=dec_seconds)
    async with state.proxy() as data:
        minutes = data.get('minutes')
    await Pace.next()
    await bot.send_message(user_id, text=f'Темп тренировки: {minutes}:{dec_seconds}x мин/ км.',
                           reply_markup=digital_keyboard)


@dp.message_handler(lambda msg: msg.text.isdigit() and int(msg.text) < 10, state=Pace.seconds)
async def pace_form_third_digit(msg: types.Message, state: FSMContext):

    user_id = msg.from_user.id
    seconds = int(msg.text)

    await state.update_data(seconds=seconds)
    async with state.proxy() as data:
        minutes = data.get('minutes')
        dec_second = data.get('dec_seconds')
        interval = data.get('interval')
        long = data.get('long')
    await Pace.next()

    await bot.send_message(user_id, text=f'Темп тренировки: {minutes}:{dec_second}{seconds} мин/км.',
                           reply_markup=types.ReplyKeyboardRemove())
    pace1k = int(minutes) * 60 + int(dec_second) * 10 + int(seconds)
    total = ''
    if interval:
        total = interval_charts(pace=pace1k)
    elif long:
        total = long_charts(pace=pace1k)
    await bot.send_message(user_id, text=total, reply_markup=finish_keyboard)
