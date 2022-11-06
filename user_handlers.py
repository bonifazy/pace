from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import date
import logging

from loader import dp, bot
from db import Users
from settings import LOG_FILE
from filters import IsUserPersonal
from message import MESSAGE
from user_features import Chart


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

next_step_keyboard = types.InlineKeyboardMarkup()
interval_menu = types.InlineKeyboardButton(text='/interval', callback_data='menu_interval')
tempo_menu = types.InlineKeyboardButton(text='/tempo', callback_data='menu_tempo')
long_menu = types.InlineKeyboardButton(text='/long', callback_data='menu_long')
next_step_keyboard.row(interval_menu, tempo_menu, long_menu)


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
    """
    Get menu in text message, duplicate system Telegram menu button.
    """
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


@dp.message_handler(IsUserPersonal(), commands=['interval'])
async def interval(msg: types.Message, state: FSMContext):
    """
    Get intervals workout distance charts by pace
    """
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
    await bot.send_message(user_id, text=MESSAGE['new_pace'], reply_markup=digital_keyboard, parse_mode='Markdown')

    log.info(f'{first_name} push /interval button.')


@dp.message_handler(IsUserPersonal(), commands=['tempo'])
async def tempo(msg: types.Message, state: FSMContext):
    """
    Get tempo run distance charts by pace
    """
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_name = msg.from_user.username
    today = date.today().strftime('%Y-%m-%d')
    info = (first_name, user_name, today)

    # new user to db or update user info: username and login date
    with Users() as users:
        users[user_id] = info

    await state.finish()  # clear any active states before
    await state.update_data(tempo=True)  # set only this distance calculation
    await Pace.wait_digit.set()
    await bot.send_message(user_id, text=MESSAGE['new_pace'], reply_markup=digital_keyboard, parse_mode='Markdown')

    log.info(f'{first_name} push /tempo button.')


@dp.message_handler(IsUserPersonal(), commands=['long'])
async def long(msg: types.Message, state: FSMContext):
    """
    Get long run distance charts by pace
    """
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_name = msg.from_user.username
    today = date.today().strftime('%Y-%m-%d')
    info = (first_name, user_name, today)

    # new user to db or update user info: username and login date
    with Users() as users:
        users[user_id] = info

    await state.finish()  # clear any active states before
    await state.update_data(long=True)  # set only this distance calculation
    await Pace.wait_digit.set()

    await bot.send_message(user_id, text=MESSAGE['new_pace'], reply_markup=digital_keyboard, parse_mode='Markdown')

    log.info(f'{first_name} push /long button.')


@dp.message_handler(IsUserPersonal(), commands=['help'])
async def user_help(msg: types.Message):
    """
    Get bot bio and project github and admin link
    """
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name

    await bot.send_message(user_id, text=MESSAGE['help'])
    log.info(f'{first_name} push /help button.')


@dp.message_handler(IsUserPersonal(), commands=['start', 'pace', 'tempo', 'long', 'help'], state=Pace.wait_digit)
async def callback_cancelled_enter_digits(msg: types.Message, state: FSMContext):
    """
    Callback handler in situations where active waiting mode digital keyboard to get pace (by three digits)
    and user want to cancel this actions, for example, push another menu buttons (not this digital keyboard).
    Clear waiting enter pace mode and redirect to main menu buttons.
    """
    await state.reset_state(with_data=True)

    if msg.text == '/start':
        await start(msg=msg)
    elif msg.text == '/pace':
        await interval(msg=msg, state=state)
    elif msg.text == '/tempo':
        await tempo(msg=msg, state=state)
    elif msg.text == '/long':
        await long(msg=msg, state=state)
    elif msg.text == '/help':
        await user_help(msg=msg)


@dp.callback_query_handler(lambda call: call.data[-1].isdigit(), state=Pace.wait_digit)
async def callback_pace_from_inline_keyboard(call: types.CallbackQuery, state: FSMContext):
    """
    Digital keyboard callback handler
    """

    user_id = call.from_user.id
    wait_digit = int(call.data[-1])

    async with state.proxy() as data:
        first_digit = data.get('first_digit')
        second_digit = data.get('second_digit')
        third_digit = data.get('third_digit')

    # get first digit in pace -> is minutes (in entered x:xx min/ km template pace)
    if first_digit is None and second_digit is None and third_digit is None:
        # bad minutes value: from 0:00 min/ km to 2:00 min/ km
        if wait_digit == 0 or wait_digit == 1:
            await Pace.wait_digit.set()
            await bot.edit_message_text(text=f'Ошибка ввода минут! \n'
                                             f'Принимается темп от 2:00мин/км. до 9:59мин/км. \n'
                                             'Введите минуты от 2 до 9:', chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard)
        # minutes: correct value from 2:00 to 9:59 min/ km.
        else:
            await state.update_data(first_digit=wait_digit)
            pace = f'{wait_digit}:xx'
            await Pace.wait_digit.set()
            await bot.edit_message_text(text=f'Ваш темп: *{pace}* мин/км. \n'
                                             'Введите темп тремя цифрами:',
                                        chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard,
                                        parse_mode='Markdown')

    # get second digit in pace, is ten of seconds of entered pace
    elif first_digit is not None and second_digit is None and third_digit is None:

        # ten of seconds: correct value from 00 to 59 sec.
        if wait_digit < 6:
            await state.update_data(second_digit=wait_digit)
            pace = f'{first_digit}:{wait_digit}x'
            await Pace.wait_digit.set()
            await bot.edit_message_text(text=f'Ваш темп: *{pace}* мин/км.\n'
                                             'Введите темп тремя цифрами:',
                                        chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard,
                                        parse_mode='Markdown')
        # bad ten seconds value: from x:60 to x:99 seconds
        else:
            await Pace.wait_digit.set()
            await bot.edit_message_text(text=f'Ошибка ввода десятков секунд!\n'
                                             f'Принимается темп от {first_digit}:00мин/км. до '
                                             f'{first_digit}:59мин/км.\n'
                                             'Введите десятки секунд от от 0 до 5:', chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard)

    # get third digit in pace, is seconds
    # if ok, then calculate all entered values by final_calculation function
    elif first_digit is not None and second_digit is not None and third_digit is None:

        # seconds: any digit is correct value
        await state.update_data(third_digit=wait_digit)
        pace = f'{first_digit}:{second_digit}{wait_digit}'
        await state.reset_state(with_data=False)
        sec_pace = first_digit * 60 + second_digit * 10 + wait_digit
        await bot.edit_message_text(text=f'Ваш темп: *{pace}* мин/км.\n'
                                         'Введите темп тремя цифрами:',
                                    chat_id=user_id,
                                    message_id=call.message.message_id,
                                    reply_markup=digital_keyboard,
                                    parse_mode='Markdown')

        # final feature calculation
        await final_calculation(user_id=user_id, pace=sec_pace, state=state)

    # send to Telegram correct work with callback handler
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda call: call.data.startswith('menu_'), state='*')
async def callback_next_step_menu(call: types.CallbackQuery, state: FSMContext):
    """
    footer menu buttons callback handler
    """
    # if user press footer line buttons
    if call.data.endswith('interval'):
        await interval(msg=call, state=state)
    if call.data.endswith('tempo'):
        await tempo(msg=call, state=state)
    if call.data.endswith('long'):
        await long(msg=call, state=state)

    # send to Telegram correct work with callback handler
    await bot.answer_callback_query(call.id)


async def final_calculation(user_id: int, pace: int, state: FSMContext):
    """
    Calculate distance charts by entered pace
    """
    chart = Chart(pace=pace)
    result_charts = ''

    async with state.proxy() as data:
        if data.get('interval'):
            result_charts = chart.interval
        elif data.get('tempo'):
            result_charts = chart.tempo
        elif data.get('long'):
            result_charts = chart.long
    await state.reset_state(with_data=True)
    await bot.send_message(user_id, text=result_charts, parse_mode='Markdown')
    await bot.send_message(user_id, text='Новая раскладка:', reply_markup=next_step_keyboard)
