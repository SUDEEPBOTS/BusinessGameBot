from pyrogram import filters
from pyrogram.types import Message
from BUSINESS.core.bot import app
from BUSINESS import config

@app.on_message(filters.command("gban") & filters.user(config.SUDOERS))
async def gban_command(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to global ban them.")
    user_id = message.reply_to_message.from_user.id
    if user_id in config.SUDOERS:
        return await message.reply_text("You cannot gban a sudo user.")
    if user_id in config.BANNED_USERS:
        return await message.reply_text("This user is already globally banned.")
    config.BANNED_USERS.append(user_id)
    await message.reply_text(f"Globally banned {message.reply_to_message.from_user.mention} from using the bot!")

@app.on_message(filters.command("ungban") & filters.user(config.SUDOERS))
async def ungban_command(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to remove global ban.")
    user_id = message.reply_to_message.from_user.id
    if user_id not in config.BANNED_USERS:
        return await message.reply_text("This user is not globally banned.")
    config.BANNED_USERS.remove(user_id)
    await message.reply_text(f"Global ban removed for {message.reply_to_message.from_user.mention}.")