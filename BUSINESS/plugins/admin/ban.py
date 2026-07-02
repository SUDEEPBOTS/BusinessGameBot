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
from pyrogram.enums import ChatMemberStatus
from BUSINESS.core.bot import app
from BUSINESS.utils.logger import play_logs

async def check_admin(message: Message) -> bool:
    member = await app.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]

@app.on_message(filters.command("ban") & filters.group)
async def ban_command(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    if not await check_admin(message):
        return await app.send_message(message.chat.id, "You must be an admin to use this command.")
    await play_logs(message, "ban")
    if not message.reply_to_message:
        return await app.send_message(message.chat.id, "Reply to a user to ban them.")
    user_id = message.reply_to_message.from_user.id
    try:
        await app.ban_chat_member(message.chat.id, user_id)
        await app.send_message(message.chat.id, f"Successfully banned {message.reply_to_message.from_user.mention}.")
    except Exception as e:
        await app.send_message(message.chat.id, f"Failed to ban: {e}")

@app.on_message(filters.command("unban") & filters.group)
async def unban_command(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    if not await check_admin(message):
        return await app.send_message(message.chat.id, "You must be an admin to use this command.")
    await play_logs(message, "unban")
    if not message.reply_to_message:
        return await app.send_message(message.chat.id, "Reply to a user to unban them.")
    user_id = message.reply_to_message.from_user.id
    try:
        await app.unban_chat_member(message.chat.id, user_id)
        await app.send_message(message.chat.id, f"Successfully unbanned {message.reply_to_message.from_user.mention}.")
    except Exception as e:
        await app.send_message(message.chat.id, f"Failed to unban: {e}")