from aiogram import executor
import logging

from loader import dp
from settings import LOG_FILE
import admin_handlers
import user_handlers


logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    filemode='a',
                    datefmt='%Y-%m-%d, %H:%M',
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')
log = logging.getLogger('Bot')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
