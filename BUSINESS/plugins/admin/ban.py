from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from BUSINESS.core.bot import app
from BUSINESS.utils.logger import play_logs

async def check_admin(message: Message) -> bool:
    member = await app.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]

@app.on_message(filters.command("ban") & filters.group)
async def ban_command(client, message: Message):
    if not await check_admin(message):
        return await message.reply_text("You must be an admin to use this command.")
    
    await play_logs(message, "ban")
    
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to ban them.")
        
    user_id = message.reply_to_message.from_user.id
    
    try:
        await app.ban_chat_member(message.chat.id, user_id)
        await message.reply_text(f"Successfully banned {message.reply_to_message.from_user.mention}.")
    except Exception as e:
        await message.reply_text(f"Failed to ban: {e}")

@app.on_message(filters.command("unban") & filters.group)
async def unban_command(client, message: Message):
    if not await check_admin(message):
        return await message.reply_text("You must be an admin to use this command.")
        
    await play_logs(message, "unban")
    
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to unban them.")
        
    user_id = message.reply_to_message.from_user.id
    
    try:
        await app.unban_chat_member(message.chat.id, user_id)
        await message.reply_text(f"Successfully unbanned {message.reply_to_message.from_user.mention}.")
    except Exception as e:
        await message.reply_text(f"Failed to unban: {e}")
