# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.
#
# This code is the intellectual property of SUDEEPBOTS.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: sudeepgithub@gmail.com

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from BUSINESS.core.bot import app
from BUSINESS.database.db import db
import config
from BUSINESS.utils.fonts import button_font
from BUSINESS.utils.language import get_string
from BUSINESS.utils.logger import play_logs

@app.on_message(filters.command(["start", "help"]))
async def start_command(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    await play_logs(message, "start")
    
    if message.chat.id != message.from_user.id:
        button = [[InlineKeyboardButton(text="Click Here For Help Menu", url=f"https://t.me/{app.me.username}?start=help")]]
        return await app.send_message(message.chat.id, 
            "Contact me in PM to view the help menu!",
            reply_markup=InlineKeyboardMarkup(button)
        )
        
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
    buttons = [
        [
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_ADD_ME")), url=f"https://t.me/{app.me.username}?startgroup=true"),
        ],
        [
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_HELP")), callback_data="help_menu"),
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_ABOUT")), callback_data="about_menu"),
        ],
        [
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_SUPPORT")), url="https://t.me/yuki_support"),
            InlineKeyboardButton(text=button_font(get_string(lang, "BTN_OWNER")), url=f"tg://user?id={config.OWNER_ID}")
        ]
    ]
    await app.send_photo(message.chat.id, 
        photo=config.START_IMG_URL,
        caption=get_string(lang, "START_TEXT"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )