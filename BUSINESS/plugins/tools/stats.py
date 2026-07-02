import psutil
from pyrogram import filters
from pyrogram.types import Message
from BUSINESS.core.bot import app
import config

@app.on_message(filters.command("stats") & filters.user(config.SUDOERS))
async def stats_command(client, message: Message):
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
    await message.reply_text(stats_text)