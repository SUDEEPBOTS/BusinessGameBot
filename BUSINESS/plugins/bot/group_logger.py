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
from pyrogram.types import Message
from BUSINESS.core.bot import app
import config

@app.on_message(filters.new_chat_members)
async def on_bot_added(client, message: Message):
    try:
        if not config.LOGGER_ID:
            return
        for member in message.new_chat_members:
            if member.id == app.me.id:
                added_by = message.from_user.mention if message.from_user else "Unknown User"
                chat = message.chat
                log_text = f"""
#NEW_GROUP
**Business Game Bot added to a group!**

**Group Name:** {chat.title}
**Group ID:** `{chat.id}`
**Added By:** {added_by}
**Members:** {await app.get_chat_members_count(chat.id)}
"""
                await app.send_message(config.LOGGER_ID, text=log_text)
                await message.reply_text("Thanks for adding me! Type /business to start a game lobby. 🎲🏦")
    except Exception as e:
        print(f"Error in on_bot_added: {e}")

@app.on_message(filters.left_chat_member)
async def on_bot_removed(client, message: Message):
    try:
        if not config.LOGGER_ID:
            return
        if message.left_chat_member.id == app.me.id:
            removed_by = message.from_user.mention if message.from_user else "Unknown User"
            chat = message.chat
            log_text = f"""
#LEFT_GROUP
**Business Game Bot was removed from a group!**

**Group Name:** {chat.title}
**Group ID:** `{chat.id}`
**Removed By:** {removed_by}
"""
            await app.send_message(config.LOGGER_ID, text=log_text)
    except Exception as e:
        print(f"Error in on_bot_removed: {e}")