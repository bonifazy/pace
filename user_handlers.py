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
from buttons import digital_keyboard, next_step_keyboard, competitions_keyboard, distance_training_keyboard


logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    filemode='a',
                    datefmt='%Y-%m-%d, %H:%M',
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')
log = logging.getLogger('Bot')


class Pace(StatesGroup):
    wait_pace = State()
    wait_time = State()
    first_digit = State()
    second_digit = State()
    third_digit = State()
    interval = State()
    tempo = State()
    long = State()
    competitions = State()
    distance_training = State()


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


@dp.message_handler(IsUserPersonal(), commands=['pace'])
async def pace(msg: types.Message):

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_name = msg.from_user.username
    today = date.today().strftime('%Y-%m-%d')
    info = (first_name, user_name, today)

    # new user to db or update user info: username and login date
    with Users() as users:
        users[user_id] = info

    await bot.send_message(user_id, text=MESSAGE['pace'])

    log.info(f'{first_name} push /pace button.')


@dp.message_handler(IsUserPersonal(), commands=['distance'])
async def distance_training(msg: types.Message):
    """
    Get competitions distance charts by pace
    """
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_name = msg.from_user.username
    today = date.today().strftime('%Y-%m-%d')
    info = (first_name, user_name, today)

    # new user to db or update user info: username and login date
    with Users() as users:
        users[user_id] = info

    await bot.send_message(user_id, text=MESSAGE['distance'], reply_markup=distance_training_keyboard)

    log.info(f'{first_name} push /distance button.')


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

    await state.update_data(interval=True)
    await Pace.wait_pace.set()
    await bot.send_message(user_id, text=MESSAGE['new_pace'], reply_markup=digital_keyboard)

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

    await state.update_data(tempo=True)  # set only this distance calculation
    await Pace.wait_pace.set()
    await bot.send_message(user_id, text=MESSAGE['new_pace'], reply_markup=digital_keyboard)

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

    await state.update_data(long=True)  # set only this distance calculation
    await Pace.wait_pace.set()

    await bot.send_message(user_id, text=MESSAGE['new_pace'], reply_markup=digital_keyboard)

    log.info(f'{first_name} push /long button.')


@dp.message_handler(IsUserPersonal(), commands=['competitions'])
async def competitions(msg: types.Message):
    """
    Get competitions distance charts by pace
    """
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_name = msg.from_user.username
    today = date.today().strftime('%Y-%m-%d')
    info = (first_name, user_name, today)

    # new user to db or update user info: username and login date
    with Users() as users:
        users[user_id] = info

    await bot.send_message(user_id, text=MESSAGE['competitions'], reply_markup=competitions_keyboard)

    log.info(f'{first_name} push /competitions button.')


@dp.message_handler(IsUserPersonal(), commands=['help'])
async def user_help(msg: types.Message):
    """
    Get bot bio and project github and admin link
    """
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name

    await bot.send_message(user_id, text=MESSAGE['help'])
    log.info(f'{first_name} push /help button.')


@dp.message_handler(IsUserPersonal(),
                    commands=['start', 'pace', 'distance', 'interval', 'tempo', 'long', 'competitions', 'help'],
                    state='*'
                    )
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
        await pace(msg=msg)
    elif msg.text == '/distance':
        await distance_training(msg=msg)
    elif msg.text == '/interval':
        await interval(msg=msg, state=state)
    elif msg.text == '/tempo':
        await tempo(msg=msg, state=state)
    elif msg.text == '/long':
        await long(msg=msg, state=state)
    elif msg.text == '/competitions':
        await competitions(msg=msg)
    elif msg.text == '/help':
        await user_help(msg=msg)


@dp.callback_query_handler(lambda call: call.data[-1].isdigit(), state=Pace.wait_pace)
async def callback_pace_from_inline_keyboard(call: types.CallbackQuery, state: FSMContext):
    """
    Digital keyboard callback handler
    """

    user_id = call.from_user.id
    message_id = call.message.message_id
    wait_digit = int(call.data[-1])

    async with state.proxy() as data:
        first_digit = data.get('first_digit')
        second_digit = data.get('second_digit')
        third_digit = data.get('third_digit')

    # get first digit in pace -> is minutes (in entered x:xx min/ km template pace)
    if first_digit is None:
        # bad minutes value: from 0:00 min/ km to 2:00 min/ km
        if wait_digit == 0 or wait_digit == 1:
            await Pace.wait_pace.set()
            await bot.edit_message_text(text=f'Ошибка ввода минут! \n'
                                             f'Принимается темп от 2:00мин/ км. до 9:59мин/ км. \n'
                                             f'Введите минуты от 2 до 9:', chat_id=user_id,
                                        message_id=message_id,
                                        reply_markup=digital_keyboard)
        # minutes: correct value from 2:00 to 9:59 min/ km.
        else:
            await state.update_data(first_digit=wait_digit)
            current_pace = f'{wait_digit}:xx'
            await Pace.wait_pace.set()
            await bot.edit_message_text(text=f'Введите темп тремя цифрами: \n{current_pace} мин/ км.',
                                        chat_id=user_id,
                                        message_id=message_id,
                                        reply_markup=digital_keyboard)

    # get second digit in pace, is ten of seconds of entered pace
    elif second_digit is None:
        # ten of seconds: correct value from 00 to 59 sec.
        if wait_digit < 6:
            await state.update_data(second_digit=wait_digit)
            current_pace = f'{first_digit}:{wait_digit}x'
            await Pace.wait_pace.set()
            await bot.edit_message_text(text=f'Введите темп тремя цифрами: \n{current_pace} мин/ км. \n',
                                        chat_id=user_id,
                                        message_id=message_id,
                                        reply_markup=digital_keyboard)
        # bad ten seconds value: from x:60 to x:99 seconds
        else:
            await Pace.wait_pace.set()
            await bot.edit_message_text(text=f'Ошибка ввода десятков секунд! \n'
                                             f'Принимается темп от {first_digit}:00мин/ км. до '
                                             f'{first_digit}:59мин/ км. \n'
                                             f'Введите десятки секунд от от 0 до 5:', chat_id=user_id,
                                        message_id=message_id,
                                        reply_markup=digital_keyboard)

    # get third digit in pace, is seconds
    # if ok, then calculate all entered values by final_calculation function
    elif third_digit is None:
        await state.reset_state(with_data=False)
        total_pace = first_digit * 60 + second_digit * 10 + wait_digit

        # final feature calculation
        await final_calculation(user_id=user_id, message_id=message_id, total_pace=total_pace, state=state)

    # send to Telegram correct work with callback handler
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda call: call.data[-1].isdigit(), state=Pace.wait_time)
async def callback_time_from_inline_keyboard(call: types.CallbackQuery, state: FSMContext):
    """
    Distance_training wait time keyboard callback handler
    """

    user_id = call.from_user.id
    digit = int(call.data[-1])

    async with state.proxy() as data:
        first_digit = data.get('first_digit')
        second_digit = data.get('second_digit')
        third_digit = data.get('third_digit')
        distance = data.get('distance_training')

    if first_digit is None:
        if digit in (0, 1, 2):
            await state.update_data(first_digit=digit)
            text = MESSAGE['distance_enter_time'] + f'\n{digit}x: xx мин.\n'
            await bot.edit_message_text(text=text,
                                        chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard)
        # bad minutes value or pass first zero digit
        else:
            await state.update_data(first_digit=0)
            await state.update_data(second_digit=digit)
            text = MESSAGE['distance_enter_time'] + f'\n{0}{digit}: xx мин.'
            await bot.edit_message_text(text=text,
                                        chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard)
    elif second_digit is None:
        await state.update_data(second_digit=digit)
        text = MESSAGE['distance_enter_time'] + f'\n{first_digit}{digit}: xx мин.'
        await bot.edit_message_text(text=text,
                                    chat_id=user_id,
                                    message_id=call.message.message_id,
                                    reply_markup=digital_keyboard)
    elif third_digit is None:
        if digit in (0, 1, 2, 3, 4, 5):
            await state.update_data(third_digit=digit)
            text = MESSAGE['distance_enter_time'] + f'\n{first_digit}{second_digit}: {digit}x мин.'
            await bot.edit_message_text(text=text,
                                        chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard)
        else:
            await bot.edit_message_text(text=MESSAGE['pace_form_invalid_dec_seconds_6_to_9'],
                                        chat_id=user_id,
                                        message_id=call.message.message_id,
                                        reply_markup=digital_keyboard)
    await Pace.wait_time.set()

    if first_digit is not None and second_digit is not None and third_digit is not None:
        total_time = first_digit * 600 + second_digit * 60 + third_digit * 10 + digit
        await state.reset_state(with_data=False)
        text = f'Итоговое время: {first_digit}{second_digit}: {third_digit}{digit} мин.'
        await bot.edit_message_text(text=text,
                                    chat_id=user_id,
                                    message_id=call.message.message_id)
        await distance_calculation(user_id=user_id, distance=distance, total_time=total_time)

    # send to Telegram correct work with callback handler
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda call: call.data.startswith('menu_'), state='*')
async def callback_next_step_menu(call: types.CallbackQuery, state: FSMContext):
    """
    footer menu buttons callback handler
    """

    user_id = call.from_user.id
    message_id = call.message.message_id
    await state.reset_state(with_data=True)

    # if user press footer line buttons
    if call.data.endswith('interval'):
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text='/interval')
        await interval(msg=call, state=state)
    elif call.data.endswith('tempo'):
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text='/tempo')
        await tempo(msg=call, state=state)
    elif call.data.endswith('long'):
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text='/long')
        await long(msg=call, state=state)
    elif call.data.endswith('competitions'):
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text='/competitions')
        await competitions(msg=call)
    elif call.data.endswith('distance'):
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text='/distance')
        await distance_training(msg=call)

    # send to Telegram correct work with callback handler
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda call: call.data.startswith('competitions_'))
async def callback_competitions_choice_menu(call: types.CallbackQuery, state: FSMContext):
    """
    competitions distance choice buttons callback handler
    """
    if call.data.endswith('3km'):
        await state.update_data(competitions=3)
        await bot.send_message(call.from_user.id, 'Дистанция: 3000 м.')
    elif call.data.endswith('5km'):
        await state.update_data(competitions=5)
        await bot.send_message(call.from_user.id, 'Дистанция: 5000 м.')
    elif call.data.endswith('10km'):
        await state.update_data(competitions=10)
        await bot.send_message(call.from_user.id, 'Дистанция: 10 км.')
    elif call.data.endswith('21km'):
        await state.update_data(competitions=21)
        await bot.send_message(call.from_user.id, 'Дистанция: Полумарафон, 21.1 км.')
    elif call.data.endswith('42km'):
        await state.update_data(competitions=42)
        await bot.send_message(call.from_user.id, 'Дистанция: Марафон, 42.2 км.')
    await Pace.wait_pace.set()
    await bot.send_message(call.from_user.id, MESSAGE['new_pace'], reply_markup=digital_keyboard)

    # send to Telegram correct work with callback handler
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda call: call.data.startswith('distance_training_'), state='*')
async def callback_distance_training_choice_menu(call: types.CallbackQuery, state: FSMContext):
    """
    competitions distance choice buttons callback handler
    """
    if call.data.endswith('400m'):
        await state.update_data(distance_training=400)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 400 м.')
    elif call.data.endswith('0500m'):
        await state.update_data(distance_training=500)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 500 м.')
    elif call.data.endswith('0600m'):
        await state.update_data(distance_training=600)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 600 м.')
    elif call.data.endswith('800m'):
        await state.update_data(distance_training=800)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 800 м.')
    elif call.data.endswith('1000m'):
        await state.update_data(distance_training=1000)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 1000 м.')
    elif call.data.endswith('1200m'):
        await state.update_data(distance_training=1200)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 1200 м.')
    elif call.data.endswith('1500m'):
        await state.update_data(distance_training=1500)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 1500 м.')
    elif call.data.endswith('1600m'):
        await state.update_data(distance_training=1600)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 1600 м.')
    elif call.data.endswith('2km'):
        await state.update_data(distance_training=2000)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 2 км.')
    elif call.data.endswith('3km'):
        await state.update_data(distance_training=3000)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 3 км.')
    elif call.data.endswith('4km'):
        await state.update_data(distance_training=4000)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 4 км.')
    elif call.data.endswith('5km'):
        await state.update_data(distance_training=5000)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Дистанция: 5 км.')

    await Pace.wait_time.set()
    text = MESSAGE['distance_enter_time'] + '\nxx мин: xx сек.'
    await bot.send_message(call.from_user.id, text=text, reply_markup=digital_keyboard)

    # send to Telegram correct work with callback handler
    await bot.answer_callback_query(call.id)


async def final_calculation(user_id: int, message_id: int, total_pace: int, state: FSMContext):
    """
    Calculate distance charts by entered pace
    """
    chart = Chart(pace=total_pace)
    result_charts = ''

    async with state.proxy() as data:
        if data.get('interval'):
            result_charts = chart.interval
        elif data.get('tempo'):
            result_charts = chart.tempo
        elif data.get('long'):
            result_charts = chart.long
        elif data.get('competitions'):
            distance = data.get('competitions')
            result_charts = chart.competitions(distance)
    await state.reset_state(with_data=True)
    await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=result_charts)
    await bot.send_message(user_id, text='Новая раскладка:', reply_markup=next_step_keyboard)


async def distance_calculation(user_id: int, distance: int, total_time: int):
    """
    Calculate pace by distance and its total time
    """

    chart = Chart(total_time=total_time, distance=distance)
    result = chart.laps_and_pace()
    if result is not None:
        await bot.send_message(user_id, text=result)
    else:
        await bot.send_message(user_id, text=MESSAGE['uncorrect_pace'])
    await bot.send_message(user_id, text='Новая раскладка:', reply_markup=next_step_keyboard)
