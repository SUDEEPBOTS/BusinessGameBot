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
import config
from BUSINESS.utils.fonts import button_font
from BUSINESS.utils.language import get_string
from BUSINESS.utils.logger import play_logs

@app.on_message(filters.command(["start", "help"]))
async def start_command(client, message: Message):
    await play_logs(message, "start")
    lang = "en" 
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
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=get_string(lang, "START_TEXT"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )