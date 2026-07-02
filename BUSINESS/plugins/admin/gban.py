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

@app.on_message(filters.command("gban") & filters.user(config.SUDOERS))
async def gban_command(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    if not message.reply_to_message:
        return await app.send_message(message.chat.id, "Reply to a user to global ban them.")
    user_id = message.reply_to_message.from_user.id
    if user_id in config.SUDOERS:
        return await app.send_message(message.chat.id, "You cannot gban a sudo user.")
    if user_id in config.BANNED_USERS:
        return await app.send_message(message.chat.id, "This user is already globally banned.")
    config.BANNED_USERS.append(user_id)
    await app.send_message(message.chat.id, f"Globally banned {message.reply_to_message.from_user.mention} from using the bot!")

@app.on_message(filters.command("ungban") & filters.user(config.SUDOERS))
async def ungban_command(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    if not message.reply_to_message:
        return await app.send_message(message.chat.id, "Reply to a user to remove global ban.")
    user_id = message.reply_to_message.from_user.id
    if user_id not in config.BANNED_USERS:
        return await app.send_message(message.chat.id, "This user is not globally banned.")
    config.BANNED_USERS.remove(user_id)
    await app.send_message(message.chat.id, f"Global ban removed for {message.reply_to_message.from_user.mention}.")