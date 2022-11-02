from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import date
import logging
from asyncio import sleep

from loader import dp, bot
from db import Users
from settings import LOG_FILE
from filters import IsUserPersonal
from message import MESSAGE
from user_features import interval_charts, tempo_charts, long_charts


logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    filemode='a',
                    datefmt='%Y-%m-%d, %H:%M',
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')
log = logging.getLogger('Bot')

digital_keyboard = types.InlineKeyboardMarkup()
digit_1 = types.InlineKeyboardButton(text='1', callback_data='digit_1')
digit_2 = types.InlineKeyboardButton(text='2', callback_data='digit_2')
digit_3 = types.InlineKeyboardButton(text='3', callback_data='digit_3')
digit_4 = types.InlineKeyboardButton(text='4', callback_data='digit_4')
digit_5 = types.InlineKeyboardButton(text='5', callback_data='digit_5')
digit_6 = types.InlineKeyboardButton(text='6', callback_data='digit_6')
digit_7 = types.InlineKeyboardButton(text='7', callback_data='digit_7')
digit_8 = types.InlineKeyboardButton(text='8', callback_data='digit_8')
digit_9 = types.InlineKeyboardButton(text='9', callback_data='digit_9')
digit_0 = types.InlineKeyboardButton(text='0', callback_data='digit_0')
digit_dummy = types.InlineKeyboardButton(text=' ', callback_data='digit_dummy_')
digital_keyboard.row(digit_1, digit_2, digit_3)
digital_keyboard.row(digit_4, digit_5, digit_6)
digital_keyboard.row(digit_7, digit_8, digit_9)
digital_keyboard.row(digit_dummy, digit_0, digit_dummy)


class Pace(StatesGroup):
    wait_digit = State()
    first_digit = State()
    second_digit = State()
    third_digit = State()
    interval = State()
    tempo = State()
    long = State()


@dp.message_handler(IsUserPersonal(), commands=['start'])
async def start(msg: types.Message):

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


@dp.message_handler(IsUserPersonal(), commands=['pace'])
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
    await Pace.wait_digit.set()
    await bot.send_message(user_id, text=MESSAGE['clear_pace'], reply_markup=digital_keyboard)

    log.info(f'{first_name} push /pace button.')


@dp.message_handler(IsUserPersonal(), commands=['tempo'])
async def tempo(msg: types.Message, state: FSMContext):

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_name = msg.from_user.username
    today = date.today().strftime('%Y-%m-%d')
    info = (first_name, user_name, today)

    # new user to db or update user info: username and login date
    with Users() as users:
        users[user_id] = info

    await state.finish()
    await state.update_data(tempo=True)
    await Pace.wait_digit.set()
    await bot.send_message(user_id, text=MESSAGE['clear_pace'], reply_markup=digital_keyboard)

    log.info(f'{first_name} push /tempo button.')


@dp.message_handler(IsUserPersonal(), commands=['long'])
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
    await Pace.wait_digit.set()

    await bot.send_message(user_id, text=MESSAGE['clear_pace'], reply_markup=digital_keyboard)

    log.info(f'{first_name} push /long button.')


@dp.message_handler(IsUserPersonal(), commands=['help'])
async def user_help(msg: types.Message):

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name

    await bot.send_message(user_id, text=MESSAGE['help'])
    log.info(f'{first_name} push /help button.')


@dp.message_handler(IsUserPersonal(), commands=['start', 'pace', 'tempo', 'long', 'help'], state=Pace.wait_digit)
async def callback_cancelled_enter_digits(msg: types.Message, state: FSMContext):

    await state.reset_state(with_data=True)

    if msg.text == '/start':
        await start(msg=msg)
    elif msg.text == '/pace':
        await pace(msg=msg, state=state)
    elif msg.text == '/tempo':
        await tempo(msg=msg, state=state)
    elif msg.text == '/long':
        await long(msg=msg, state=state)
    elif msg.text == '/help':
        await user_help(msg=msg)


@dp.callback_query_handler(lambda call: call.data[-1].isdigit(), state=Pace.wait_digit)
async def callback_pace_from_inline_keyboard(call: types.CallbackQuery, state: FSMContext):

    user_id = call.from_user.id
    wait_digit = int(call.data[-1])

    async with state.proxy() as data:
        first_digit = data.get('first_digit')
        second_digit = data.get('second_digit')
        third_digit = data.get('third_digit')

    if first_digit is None and second_digit is None and third_digit is None:

        # minutes: correct value from 2:00 to 9:59 min/ km.
        if not wait_digit == 0 and not wait_digit == 1:
            await state.update_data(first_digit=wait_digit)
            pace = f'{wait_digit}:xx'
            await Pace.wait_digit.set()
            await bot.edit_message_text(text=f'Ваш темп: {pace} мин/ км. \n'
                                             f'Введите темп тремя цифрами:',
                                        chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard)
        else:
            # bad minutes value: from 0:00 min/ km to 2:00 min/ km
            await Pace.wait_digit.set()
            await bot.edit_message_text(text=f'Ошибка ввода минут! \n'
                                             f'Принимается темп от 2:00мин/ км. до 9:59мин/ км. \n'
                                             f'Введите минуты от 2 до 9:', chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard)

    elif first_digit is not None and second_digit is None and third_digit is None:

        # dec seconds: correct value from 00 to 59 sec.
        if wait_digit < 6:
            await state.update_data(second_digit=wait_digit)
            pace = f'{first_digit}:{wait_digit}x'
            await Pace.wait_digit.set()
            await bot.edit_message_text(text=f'Ваш темп: {pace} мин/ км. \n'
                                             f'Введите темп тремя цифрами:',
                                        chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard)
        else:
            # bad dec_seconds value: from x:60 to x:99 seconds
            await Pace.wait_digit.set()
            await bot.edit_message_text(text=f'Ошибка ввода десятков секунд! \n'
                                             f'Принимается темп от {first_digit}:00мин/ км. до '
                                             f'{first_digit}:59мин/ км. \n'
                                             f'Введите десятки секунд от от 0 до 5:', chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard)

    elif first_digit is not None and second_digit is not None and third_digit is None:

        # seconds: correct value
        await state.update_data(third_digit=wait_digit)
        pace = f'{first_digit}:{second_digit}{wait_digit}'
        await state.reset_state(with_data=False)
        sec_pace = first_digit * 60 + second_digit * 10 + wait_digit
        await bot.edit_message_text(text=f'Ваш темп: {pace} мин/ км. \n'
                                         f'Введите темп тремя цифрами:',
                                    chat_id=user_id,
                                    message_id=call.message.message_id,
                                    reply_markup=digital_keyboard)
        # final calculation
        await final_calculation(user_id=user_id, pace=sec_pace, state=state)

    await bot.answer_callback_query(call.id)


async def final_calculation(user_id: int, pace: int, state: FSMContext):

    result_charts = ''

    async with state.proxy() as data:
        interval = data.get('interval')
        tempo = data.get('tempo')
        long = data.get('long')
    if interval:
        result_charts = interval_charts(pace=pace)
    elif tempo:
        result_charts = tempo_charts(pace=pace)
    elif long:
        result_charts = long_charts(pace=pace)
    await state.reset_state(with_data=True)
    await bot.send_message(user_id, text=result_charts)
    await sleep(5)
    await bot.send_message(user_id, text=MESSAGE['next_step'])
