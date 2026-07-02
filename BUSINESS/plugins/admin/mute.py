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

import time
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from BUSINESS.core.bot import app
from BUSINESS.utils.logger import play_logs
from BUSINESS.plugins.admin.ban import check_admin

@app.on_message(filters.command("mute") & filters.group)
async def mute_command(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    if not await check_admin(message):
        return await app.send_message(message.chat.id, "You must be an admin to use this command.")
    await play_logs(message, "mute")
    if not message.reply_to_message:
        return await app.send_message(message.chat.id, "Reply to a user to mute them.")
    user_id = message.reply_to_message.from_user.id
    try:
        await app.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=False))
        await app.send_message(message.chat.id, f"Successfully muted {message.reply_to_message.from_user.mention}.")
    except Exception as e:
        await app.send_message(message.chat.id, f"Failed to mute: {e}")

@app.on_message(filters.command("unmute") & filters.group)
async def unmute_command(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    if not await check_admin(message):
        return await app.send_message(message.chat.id, "You must be an admin to use this command.")
    await play_logs(message, "unmute")
    if not message.reply_to_message:
        return await app.send_message(message.chat.id, "Reply to a user to unmute them.")
    user_id = message.reply_to_message.from_user.id
    try:
        await app.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
        await app.send_message(message.chat.id, f"Successfully unmuted {message.reply_to_message.from_user.mention}.")
    except Exception as e:
        await app.send_message(message.chat.id, f"Failed to unmute: {e}")

@app.on_message(filters.command("tmute") & filters.group)
async def tmute_command(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    if not await check_admin(message):
        return await app.send_message(message.chat.id, "You must be an admin to use this command.")
    await play_logs(message, "tmute")
    if not message.reply_to_message:
        return await app.send_message(message.chat.id, "Reply to a user to tmute them.")
    if len(message.command) < 2:
        return await app.send_message(message.chat.id, "Please provide time in minutes. Example: /tmute 5")
    try:
        minutes = int(message.command[1])
        until_date = int(time.time() + (minutes * 60))
    except ValueError:
        return await app.send_message(message.chat.id, "Invalid time format. Use minutes as numbers.")
    user_id = message.reply_to_message.from_user.id
    try:
        await app.restrict_chat_member(
            message.chat.id, 
            user_id, 
            ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await app.send_message(message.chat.id, f"Successfully muted {message.reply_to_message.from_user.mention} for {minutes} minutes.")
    except Exception as e:
        await app.send_message(message.chat.id, f"Failed to mute: {e}")