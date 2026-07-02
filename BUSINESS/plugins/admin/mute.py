import time
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from BUSINESS.core.bot import app
from BUSINESS.utils.logger import play_logs
from BUSINESS.plugins.admin.ban import check_admin

@app.on_message(filters.command("mute") & filters.group)
async def mute_command(client, message: Message):
    if not await check_admin(message):
        return await message.reply_text("You must be an admin to use this command.")
        
    await play_logs(message, "mute")
    
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to mute them.")
        
    user_id = message.reply_to_message.from_user.id
    
    try:
        await app.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=False))
        await message.reply_text(f"Successfully muted {message.reply_to_message.from_user.mention}.")
    except Exception as e:
        await message.reply_text(f"Failed to mute: {e}")

@app.on_message(filters.command("unmute") & filters.group)
async def unmute_command(client, message: Message):
    if not await check_admin(message):
        return await message.reply_text("You must be an admin to use this command.")
        
    await play_logs(message, "unmute")
    
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to unmute them.")
        
    user_id = message.reply_to_message.from_user.id
    
    try:
        await app.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
        await message.reply_text(f"Successfully unmuted {message.reply_to_message.from_user.mention}.")
    except Exception as e:
        await message.reply_text(f"Failed to unmute: {e}")

@app.on_message(filters.command("tmute") & filters.group)
async def tmute_command(client, message: Message):
    if not await check_admin(message):
        return await message.reply_text("You must be an admin to use this command.")
        
    await play_logs(message, "tmute")
    
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to tmute them.")
        
    if len(message.command) < 2:
        return await message.reply_text("Please provide time in minutes. Example: /tmute 5")
        
    try:
        minutes = int(message.command[1])
        until_date = int(time.time() + (minutes * 60))
    except ValueError:
        return await message.reply_text("Invalid time format. Use minutes as numbers.")
        
    user_id = message.reply_to_message.from_user.id
    
    try:
        await app.restrict_chat_member(
            message.chat.id, 
            user_id, 
            ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await message.reply_text(f"Successfully muted {message.reply_to_message.from_user.mention} for {minutes} minutes.")
    except Exception as e:
        await message.reply_text(f"Failed to mute: {e}")
