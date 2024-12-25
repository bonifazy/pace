import sqlite3
import logging

from settings import DB_FILE, BOT_LOG

logging.basicConfig(filename=BOT_LOG,
                    level=logging.INFO,
                    filemode='a',
                    datefmt='%Y-%m-%d, %H:%M',
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')
log = logging.getLogger('database')


class Users:
    """
    build in functions:

    with.. as..:
    users = Users()
    with users as db:
        ...

    in:
    if user_id in db...

    set item:
    db[user_id] = user_info  # firstname, username, file, date

    get item:
    var = db[user_id]

    """
    
    # protection from double connectors to database. sqlite3 module don't support 2 and more parallel connections
    def __new__(cls):
        if not hasattr(cls, 'sync_db_connector'):
            cls.sync_db_connector = super(Users, cls).__new__(cls)
        return cls.sync_db_connector

    def __init__(self):
        # to real path to 'db.sqlite3' file. If database file should be a parent dir,
        # set parent_dir = Path(__file__).resolve().parent.parent
        # parent_dir = Path(__file__).resolve().parent
        # self.db = os.path.join(parent_dir, DB_FILE)  # path + file with any OS
        self.db = DB_FILE
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()

    def __contains__(self, user_id: int):
        if self.is_user(user_id):
            return True
        else:
            return False

    def __getitem__(self, user_id: int):
        if self.is_user(user_id):
            sql = "SELECT id, firstname, username, `date`, `update` FROM users WHERE id={}".format(str(user_id))
            self.cur.execute(sql)
            self.conn.commit()
            result = self.cur.fetchone()
            return result
        return None

    def __setitem__(self, user_id, info):
        first_name, user_name, today = info
        if not self.is_user(user_id):
            sql = "INSERT INTO users (id, firstname, username, `date`, `update`) VALUES (?,?,?,?,?);"
            self.cur.execute(sql, (user_id, first_name, user_name, today, today))
            self.conn.commit()
            result = self.cur.fetchone()
            return result
        else:
            sql = "UPDATE users SET firstname='{}', username='{}', `update`='{}' " \
                  "WHERE id={}".format(first_name, user_name, today, int(user_id))
            self.cur.execute(sql)
            self.conn.commit()
            result = self.cur.fetchone()
            return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None and self.cur is not None:
            self.cur.close()
            self.cur = None
            self.conn.close()
            self.conn = None

    def __del__(self):
        if self.conn is not None and self.cur is not None:
            self.cur.close()
            self.cur = None
            self.conn.close()
            self.conn = None

    def is_user(self, user_id: int):
        sql = "SELECT EXISTS(SELECT 1 FROM users WHERE id={} LIMIT 1);".format(str(user_id))
        self.cur.execute(sql)
        self.conn.commit()
        result = self.cur.fetchone()[0]
        if result == 1:
            return True
        else:
            return False

    def keys(self):
        sql = "SELECT id FROM users;"
        self.cur.execute(sql)
        self.conn.commit()
        result = [i[0] for i in self.cur.fetchall()]
        return result

    def get_users(self):
        sql = "SELECT id, firstname, username, `date`, `update` FROM users ORDER BY `date` DESC LIMIT 30;"
        self.cur.execute(sql)
        self.conn.commit()
        return self.cur.fetchall()

    def count_users(self):
        sql = "SELECT COUNT(id) FROM users;"
        self.cur.execute(sql)
        self.conn.commit()
        return self.cur.fetchone()[0]

    def get_ids(self) -> list:
        """
        returns: [(id, name), (id, name)..]
        """
        sql = "SELECT id, firstname FROM users;"
        self.cur.execute(sql)
        self.conn.commit()
        ids = [(i[0], i[1]) for i in self.cur.fetchall()]
        return ids  # [(id, name), (id, name)..]


def get_users():

    with Users() as db:
        count_users = db.count_users()
        all_users = db.get_users()
    text = 'All users: {} \n\n' \
           'New users: \n'.format(count_users)
    for i in all_users:
        info = '{}, @{}: {}, update: {} \n'.format(i[1], i[2], str(i[0]), i[4])
        text += info

    return text


def get_log(lines=25):

    with open(BOT_LOG, 'rb') as f:
        total_lines_wanted = lines
        block_size = 1024
        f.seek(0, 2)
        block_end_byte = f.tell()
        lines_to_go = total_lines_wanted
        block_number = -1
        blocks = []
        while lines_to_go > 0 and block_end_byte > 0:
            if block_end_byte - block_size > 0:
                f.seek(block_number * block_size, 2)
                blocks.append(f.read(block_size))
            else:
                f.seek(0, 0)
                blocks.append(f.read(block_end_byte))
            lines_found = blocks[-1].count(b'\n')
            lines_to_go -= lines_found
            block_end_byte -= block_size
            block_number -= 1
        all_read_text = b''.join(reversed(blocks))
        text_log = b'\n'.join(all_read_text.splitlines()[-total_lines_wanted:]).decode('utf-8')

    return text_log


def get_ids():

    db = Users()
    ids = db.get_ids()

    return ids


if __name__ == '__main__':

    # test: write to db new user
    with Users() as _users:
        _users[1] = ('Test', 'test_username', '2022-10-29')
    
    # test: get all users
    print(get_users())
    print(get_log())
