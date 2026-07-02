from pyrogram import filters
from pyrogram.types import Message
from BUSINESS.core.bot import app
import config

@app.on_message(filters.command("addsudo") & filters.user(config.OWNER_ID))
async def addsudo_command(client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a user's message to add them to sudo.")
        return
    user_id = message.reply_to_message.from_user.id
    if user_id in config.SUDOERS:
        await message.reply_text("This user is already a sudoer.")
        return
    config.SUDOERS.append(user_id)
    await message.reply_text(f"Successfully added `{user_id}` to sudoers.")

@app.on_message(filters.command("rmsudo") & filters.user(config.OWNER_ID))
async def rmsudo_command(client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a user's message to remove them from sudo.")
        return
    user_id = message.reply_to_message.from_user.id
    if user_id not in config.SUDOERS:
        await message.reply_text("This user is not a sudoer.")
        return
    if user_id == config.OWNER_ID:
        await message.reply_text("You cannot remove the owner from sudoers.")
        return

    config.SUDOERS.remove(user_id)
    await message.reply_text(f"Successfully removed `{user_id}` from sudoers.")