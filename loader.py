import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from redis import Redis
from pytz import timezone
from settings import DEBUG, TOKEN, BOT_LOG, LOG_FORMAT, LOG_DATEFMT, WEBHOOK_HOST
import filters
from db import Users


logging.basicConfig(filename=BOT_LOG, level=logging.INFO, filemode='a', datefmt=LOG_DATEFMT, format=LOG_FORMAT)
log = logging.getLogger('Bot')

bot = Bot(token=TOKEN)
redis_storage = RedisStorage2('127.0.0.1', 6379, db=0, prefix='my_pace_bot_fsm')
dp = Dispatcher(bot, storage=redis_storage)
dp.bind_filter(filters.IsAdminPersonal)
dp.bind_filter(filters.IsUserPersonal)

redis = Redis(decode_responses=True)
users = Users()

# Локальная таймзона для синхронизации системного времени в проекте
tz_local = timezone('Europe/Moscow')

# Проверить подключение к Redis, установка маркера успешности подключения - is_redis_connected
is_redis_connected = False
if hasattr(redis, 'ping'):
    if redis.ping():
        is_redis_connected = True
        print(f'Redis info: {redis} successfully started.')
else:
    print('\n*****     Внимание!     *****\n'
          'Ошибка подключения Redis.\nПроверка подключения:\n'
          'Ubuntu: "dpkg -l | grep redis",\nMacOS: "brew info redis".\n'
          'Запустите виртуальное окружение и проверьте установку Redis в pip:\n'
          '"pip list | grep redis".')


async def on_startup(_):
    if not DEBUG:
        await bot.delete_webhook()
        await bot.set_webhook('', certificate='~/pace/pacebot.run.place.crt', ip_address=WEBHOOK_HOST)


async def on_shutdown(_):
    global redis, users
    if not DEBUG:
        await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    if users.cur:
        del users
    if redis is not None:
        redis.close()
        print(f'Redis info: Connector {redis} is closed.')
        del redis
