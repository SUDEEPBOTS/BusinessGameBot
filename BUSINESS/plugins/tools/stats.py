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

import psutil
from pyrogram import filters
from pyrogram.types import Message
from BUSINESS.core.bot import app
import config

@app.on_message(filters.command("stats") & filters.user(config.SUDOERS))
async def stats_command(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    stats_text = f"""
📊 **Business Game Bot Stats** 📊

**System:**
- CPU Usage: `{cpu_usage}%`
- RAM Usage: `{ram_usage}%`

*(More game stats will be added once database is connected)*
"""
    await app.send_message(message.chat.id, stats_text)