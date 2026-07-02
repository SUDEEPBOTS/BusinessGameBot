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
from BUSINESS.database.db import db
from BUSINESS.utils.language import get_string

@app.on_message(filters.command("profile"))
async def profile_command(client, message: Message):
    if not db:
        return await message.reply_text("Database is currently offline.")
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
    target_user = message.from_user
    if message.reply_to_message and message.reply_to_message.from_user:
        target_user = message.reply_to_message.from_user
    user_data = await db.get_user(target_user.id, target_user.first_name)
    text = get_string(lang, "PROFILE_MSG").format(
        name=target_user.first_name,
        played=user_data.get("games_played", 0),
        won=user_data.get("games_won", 0),
        wealth=user_data.get("total_wealth_earned", 0),
        bankruptcies=user_data.get("bankruptcies", 0)
    )
    await message.reply_text(text, quote=True)

@app.on_message(filters.command(["top", "leaderboard"]))
async def top_command(client, message: Message):
    if not db:
        return await message.reply_text("Database is currently offline.")
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
    cursor = db.users.find().sort("games_won", -1).limit(10)
    users = await cursor.to_list(length=10)
    if not users:
        return await message.reply_text(get_string(lang, "NO_DATA"))
    text = get_string(lang, "LEADERBOARD_TITLE")
    for i, u in enumerate(users):
        name = u.get("name", "Unknown Player")
        won = u.get("games_won", 0)
        wealth = u.get("total_wealth_earned", 0)
        text += get_string(lang, "LEADERBOARD_ENTRY").format(
            rank=i+1,
            name=name,
            won=won,
            wealth=wealth
        )
    await message.reply_text(text, quote=True)