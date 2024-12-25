from pathlib import Path
from yaml import safe_load

with open('config.yml') as yaml_file:
    data = safe_load(yaml_file)

# Режим разработки: True (Debug mode)/ False (Production mode)
DEBUG = data.get('DEBUG', False)

# Основные настройки логгера
BOT_LOG = data.get('BOT_LOG', '')
LOG_FORMAT = '%(asctime)s: %(name)20s: %(funcName)20s: %(levelname)7s: %(message)s'
LOG_DATEFMT = '%d.%m, %H:%M:%S'

# Настройки для aiogram.Dispatcher
TOKEN = data.get('TOKEN', '')
WEBHOOK_HOST = data.get('WEBHOOK_HOST', '')
WEBHOOK_PATH = data.get('WEBHOOK_PATH', '')
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = data.get('WEBAPP_HOST', '')
WEBAPP_PORT = data.get('WEBAPP_PORT', 0)

# Настройки фильтра пользователей/ администраторов
ADMIN_ID = data.get('ADMIN_ID', 0)
TEST_GROUP = data.get('TEST_GROUP', list())

# Файл базы данных
DB_FILE = 'db.sqlite3'


if __name__ == '__main__':
    if not Path(BOT_LOG).is_file():
        print('BOT_LOG: check path or file exists.')
    elif not Path(DB_FILE).is_file():
        print('DB_FILE: check db exists.')
    else:
        print('All paths is correct!')
