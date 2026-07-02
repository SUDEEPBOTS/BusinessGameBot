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

@app.on_message(filters.command("lang") & filters.group)
async def lang_command(client, message: Message):
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ["creator", "administrator"]:
        return await message.reply_text("Only admins can change the group language!")
        
    buttons = [
        [InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"), InlineKeyboardButton("Hindi 🇮🇳", callback_data="lang_hi")]
    ]
    await message.reply_text("Please select the bot language for this group:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^lang_"))
async def set_lang_callback(client, callback_query):
    member = await client.get_chat_member(callback_query.message.chat.id, callback_query.from_user.id)
    if member.status not in ["creator", "administrator"]:
        return await callback_query.answer("Only admins can change the group language!", show_alert=True)
        
    lang = callback_query.data.split("_")[1]
    await db.set_group_lang(callback_query.message.chat.id, lang)
    
    if lang == "hi":
        text = "✅ **Bhasha safaltapoorvak badal di gayi!**"
    else:
        text = "✅ **Language successfully changed to English!**"
        
    await callback_query.message.edit_text(text)
