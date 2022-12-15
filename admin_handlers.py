from aiogram import types
from aiogram.utils import exceptions
from datetime import date
import logging
from asyncio import sleep
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, bot
from db import Users, get_log, get_users, get_ids
from settings import LOG_FILE, TEST_GROUP
from filters import IsAdminPersonal
from buttons import first_news_keyboard, second_news_keyboard


class AdminState(StatesGroup):
    first_news = State()
    second_news = State()
    confirm_test = State()
    confirm_all = State()


logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    filemode='a',
                    datefmt='%Y-%m-%d, %H:%M',
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')
log = logging.getLogger('Bot')


@dp.message_handler(IsAdminPersonal(), commands=['start'])
async def admin_start(msg: types.Message):

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_name = msg.from_user.username
    today = date.today().strftime('%Y-%m-%d')
    info = (first_name, user_name, today)

    await msg.reply(text=f'Привет, {first_name}! \n/users - Список пользователей \n/log - Лог приложения \n'
                         f'/news - Рассылка')

    with Users() as users:
        users[user_id] = info

    log.info(f'{first_name} push /start button.')


@dp.message_handler(IsAdminPersonal(), commands=['users'])
async def admin_get_users(msg: types.Message):

    first_name = msg.from_user.first_name

    users_list = get_users()
    await msg.reply(text=users_list)

    log.info(f'{first_name} get /users feature.')


@dp.message_handler(IsAdminPersonal(), commands=['log'])
async def admin_get_log(msg: types.Message):

    first_name = msg.from_user.first_name

    log_list = get_log()
    await msg.reply(text=log_list)

    log.info(f'{first_name} get /log feature.')


@dp.message_handler(IsAdminPersonal(), commands=['news'])
async def admin_news(msg: types.Message):

    first_name = msg.from_user.first_name

    await AdminState.first_news.set()
    await msg.reply(text='Новостная рассылка для пользователей. \nВведите первую часть:')

    log.info(f'{first_name} get /news features.')


@dp.message_handler(IsAdminPersonal(), content_types=['text'], state=AdminState.first_news)
async def get_first_news(msg: types.Message, state: FSMContext):

    if msg.text == 'Отменить':
        await state.reset_state()
        await msg.reply(text='Ввод текста отменён.', reply_markup=types.ReplyKeyboardRemove())

    elif msg.text == 'Редактировать':
        await msg.reply(text='Введите первую часть рассылки: ', reply_markup=types.ReplyKeyboardRemove())

    elif msg.text == 'Дальше':
        async with state.proxy() as data:
            first_news = data.get('first_news')
        if first_news:
            await AdminState.second_news.set()
            await msg.reply(text='Введите вторую часть рассылки:', reply_markup=types.ReplyKeyboardRemove())
        else:
            await state.reset_state()
            await msg.reply(text='Ввод текста отменён.', reply_markup=types.ReplyKeyboardRemove())

    else:
        await state.update_data(first_news=msg.text)
        await AdminState.first_news.set()
        await msg.reply(text='Первая часть рассылки сохранена. \n'
                             'Отредактируйте рассылку или нажмите "Дальше" для ввода второй части.',
                        reply_markup=first_news_keyboard)


@dp.message_handler(IsAdminPersonal(), content_types=['text'], state=AdminState.second_news)
async def get_second_news(msg: types.Message, state: FSMContext):

    user_id = msg.from_user.id
    to_redact = ('Отменить', 'Редактировать', 'Тестовая рассылка', 'Опубликовать всем')
    to_send = ('1908', '19081988')

    text = msg.text

    # сохранить рассылку (1 и 2 абзац) или отправить на ввод первого абзаца
    if text not in to_redact and text not in to_send:
        async with state.proxy() as data:
            first_news = data.get('first_news')
        await state.update_data(second_news=text)

        # сохранить рассылку и ожидать нажатие кнопок для рассылки юзерам, непосредственно
        if first_news and text:
            await AdminState.second_news.set()
            await msg.reply(text='Рассылка сохранена.', reply_markup=types.ReplyKeyboardRemove())
            await bot.send_message(user_id, text=first_news)
            await bot.send_message(user_id, text=text)
            await bot.send_message(user_id, text='Проверьте и отправьте рассылку.', reply_markup=second_news_keyboard)
        # рассылки не найдено. Запросить заново
        else:
            await AdminState.first_news.set()
            await msg.reply(text='Ошибка! \nПервая часть рассылки не найдена! \n'
                                 'Сначала введите текст первой части рассылки: ',
                            reply_markup=types.ReplyKeyboardRemove())

    # обработка кнопок
    if text in to_redact:
        result_text = ''
        if text == 'Отменить':
            await state.reset_state()
            result_text = 'Ввод текста отменён.'
        elif text == 'Редактировать':
            result_text = 'Введите вторую часть рассылки: '
        elif text == 'Тестовая рассылка':
            await state.update_data(confirm_test=True)
            result_text = 'Для подтверждения введите 1908 цифрами:'
        elif text == 'Опубликовать всем':
            await state.update_data(confirm_all=True)
            result_text = 'Для подтверждения введите 19081988 цифрами:'
        await msg.reply(text=result_text, reply_markup=types.ReplyKeyboardRemove())

    # отправить рассылку (2 сообщения)
    if text in to_send:
        async with state.proxy() as data:
            first_news = data.get('first_news')
            second_news = data.get('second_news')
            confirm_test = data.get('confirm_test')
            confirm_all = data.get('confirm_all')
        test_group_ids = TEST_GROUP
        all_ids = get_ids()
        report = dict()
        result_text = ''

        await state.update_data(confirm_test=None)
        await state.update_data(confirm_all=None)
        await state.reset_state(with_data=False)

        # тестовая рассылка
        if text == '1908':
            if first_news and second_news and confirm_test and test_group_ids:
                report = await send_news(test_group_ids, first_news, second_news)
                result_text = 'Тестовая рассылка отправлена.'
            else:
                result_text = 'Рассылка не найдена.'
        # общая рассылка
        elif text == '19081988':
            if first_news and second_news and confirm_all and all_ids:
                report = await send_news(all_ids, first_news, second_news)
                result_text = 'Общая рассылка отправлена.'
            else:
                result_text = 'Рассылка не найдена.'
        await msg.reply(text=result_text, reply_markup=types.ReplyKeyboardRemove())
        await send_report(user_id=user_id, report=report)


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> str:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return: sending status
    """

    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        result = 'blocked_by_user'
    except exceptions.ChatNotFound:
        result = 'user_not_found'
    except exceptions.RetryAfter as e:
        await sleep(3600)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        result = 'user_deactivated'
    except exceptions.TelegramAPIError:
        result = 'api_wrong'
    else:
        result = 'success'

    return result


async def send_news(clients: list, first: str, second: str) -> dict:
    """
    Send greating text to username and two messages from admin to users
    """

    report = {
        'all': len(clients)
    }

    try:
        for client in clients:
            client_id, client_name = client
            if client_name is not None and client_id != '':
                greating = f'Привет, {client_name}! 🙂 '
            else:
                greating = f'Привет! 🙂 '
            result = await send_message(user_id=client_id, text=greating)

            # Correct greating send. Next send first and seconds messages.
            if result == 'success':
                await sleep(3)
                await bot.send_message(chat_id=client_id, text=first)
                await sleep(3)
                await bot.send_message(chat_id=client_id, text=second)
            if result in report:
                report[result].append(client_id)
            else:
                report[result] = [client_id]
            await sleep(1)
    finally:
        return report


async def send_report(user_id: int, report: dict) -> None:
    """
    Send report by sending news to admin
    """

    result = ''
    if 'all' in report:
        result += f'all: {report["all"]} \n'
    if 'blocked_by_user' in report:
        result += 'blocked by user: ' + ', '.join(map(str, report['blocked_by_user'])) + '\n'
    if 'user_not_found' in report:
        result += 'user_not_found: ' + ', '.join(map(str, report['user_not_found'])) + '\n'
    if 'user_deactivated' in report:
        result += 'user_deactivated: ' + ', '.join(map(str, report['user_deactivated'])) + '\n'
    if 'api_wrong' in report:
        result += 'Telegram API wrong: ' + ', '.join(map(str, report['api_wrong'])) + '\n'
    if 'success' in report:
        result += f'success: {len(report["success"])}' + '\n'

    await bot.send_message(user_id, text=result)
