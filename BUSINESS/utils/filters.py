from pyrogram import filters
from pyrogram.types import Message
import config

async def _is_banned(_, client, message: Message):
    if not message.from_user:
        return False
    return message.from_user.id in config.BANNED_USERS

is_banned = filters.create(_is_banned)