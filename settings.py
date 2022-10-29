# Run Pace bot
# settings debug mode

from pathlib import Path

# Test bot
TOKEN = ""

LOG_FILE = 'bot.log'
DB = 'db.sqlite3'

# enter your test admin telegram_id
ADMIN_ID = 777


if __name__ == '__main__':
    if not Path(LOG_FILE).is_file():
        print('LOG_FILE: chech path or file exists.')
    elif not Path(DB).is_file():
        print('USERS_DB: check db exists.')
    else:
        print('All paths is correct!')
