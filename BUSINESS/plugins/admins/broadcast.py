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

import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from BUSINESS.core.bot import app
from BUSINESS.database.db import db
from BUSINESS.config import SUDOERS

@app.on_message(filters.command(["broadcast", "bcast"]) & filters.user(SUDOERS))
async def broadcast_command(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Please reply to a message to broadcast it.")
    if not db:
        return await message.reply_text("Database is currently offline.")
    status = await message.reply_text("Starting broadcast...")
    groups = await db.get_all_groups()
    if not groups:
        return await status.edit("No groups registered in database.")
    successful = 0
    failed = 0
    for chat_id in groups:
        try:
            await message.reply_to_message.copy(chat_id)
            successful += 1
            await asyncio.sleep(0.1) 
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await message.reply_to_message.copy(chat_id)
            successful += 1
        except Exception:
            failed += 1
    await status.edit(f"✅ **Broadcast Completed!**\n\n**Total Groups:** {len(groups)}\n**Successful:** {successful}\n**Failed:** {failed}")