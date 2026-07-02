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
