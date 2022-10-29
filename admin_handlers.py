from aiogram import types
from datetime import date
import logging

from loader import dp
from db import Users, get_log, get_users
from settings import LOG_FILE
from filters import IsAdminPersonal


logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    filemode='a',
                    datefmt='%Y-%m-%d, %H:%M',
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')
log = logging.getLogger('Bot')


@dp.message_handler(IsAdminPersonal(), commands=['start', 'admin'])
async def admin(msg: types.Message):

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    user_name = msg.from_user.username
    today = date.today().strftime('%Y-%m-%d')
    info = (first_name, user_name, today)

    await msg.reply(text=f'Привет, {first_name}! \n'
                         f'/users - Список пользователей \n'
                         f'/log - Лог приложения')

    with Users() as users:
        users[user_id] = info

    log.info(f'{first_name} push /start or /admin button.')


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
