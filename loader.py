from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import TOKEN, LOG_FILE
import logging

import filters


logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    filemode='a',
                    datefmt='%Y-%m-%d, %H:%M',
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')
log = logging.getLogger('Loader')
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.bind_filter(filters.IsAdminPersonal)
dp.bind_filter(filters.IsUserPersonal)

