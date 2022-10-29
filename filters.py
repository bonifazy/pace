from aiogram.dispatcher.filters import Filter
from aiogram import types

from settings import ADMIN_ID


class IsAdminPersonal(Filter):
    key = 'is_admin_personal_chat'

    async def check(self, msg: types.Message) -> bool:
        chat_type = msg.chat.type

        return msg.from_user.id == ADMIN_ID and chat_type != 'group' and chat_type != 'supergroup'


class IsUserPersonal(Filter):
    key = 'is_user_personal_chat'

    async def check(self, msg: types.Message) -> bool:
        chat_type = msg.chat.type

        return msg.from_user.id != ADMIN_ID and chat_type != 'group' and chat_type != 'supergroup'
