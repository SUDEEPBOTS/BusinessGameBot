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

import random
from pyrogram.types import InlineKeyboardButton
from pyrogram.enums import ButtonStyle


PREMIUM_EMOJIS = [
    "5238162283368035495", 
    "5408916593780470262",
    "5409262351532701571",
    "5409042015415448331",
    "6294287714887933094",
    "6291837599254322363",
    "6294047505957003963",
]


STYLES = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]

def get_random_style():
    return random.choice(STYLES)

def get_random_emoji():
    return random.choice(PREMIUM_EMOJIS)


original_init = InlineKeyboardButton.__init__

def patched_init(self, text: str, callback_data: str = None, url: str = None,
                 web_app=None, login_url=None, user_id=None, switch_inline_query=None,
                 switch_inline_query_current_chat=None, callback_game=None, 
                 requires_password=None, pay=None, style=None, icon_custom_emoji_id=None, copy_text=None):
    if style is None:
        style = get_random_style()
    if icon_custom_emoji_id is None:
        icon_custom_emoji_id = get_random_emoji()

    original_init(self, text=text, callback_data=callback_data, url=url,
                  web_app=web_app, login_url=login_url, user_id=user_id, 
                  switch_inline_query=switch_inline_query,
                  switch_inline_query_current_chat=switch_inline_query_current_chat,
                  callback_game=callback_game, requires_password=requires_password, pay=pay, style=style, 
                  icon_custom_emoji_id=icon_custom_emoji_id, copy_text=copy_text)


InlineKeyboardButton.__init__ = patched_init