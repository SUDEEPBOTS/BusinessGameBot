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
from pyrogram.types import Message
from BUSINESS.core.bot import app

@app.on_message(filters.command("ping"))
async def ping_command(client, message: Message):
    start_time = time.time()
    msg = await message.reply_text("Pinging...")
    end_time = time.time()
    latency = round((end_time - start_time) * 1000)
    await msg.edit_text(f"**Pong!** 🏓\nLatency: `{latency}ms`")