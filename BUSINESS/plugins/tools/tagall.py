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
from BUSINESS.core.bot import app

# Global dict to keep track of active tagall processes so they can be cancelled
TAG_ALL_PROCESSES = {}

@app.on_message(filters.command(["tagall", "all"]) & filters.group)
async def tag_all(client, message: Message):
    chat_id = message.chat.id
    
    # Ensure only admins can use tagall
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in ["creator", "administrator"]:
        return await message.reply_text("Only admins can use the /tagall command.")
        
    if chat_id in TAG_ALL_PROCESSES and TAG_ALL_PROCESSES[chat_id]:
        return await message.reply_text("A tagall process is already running! Use /cancel to stop it.")
        
    TAG_ALL_PROCESSES[chat_id] = True
    
    text = ""
    if len(message.command) > 1:
        text = message.text.split(None, 1)[1]
        
    await message.reply_text("⏳ **Tagging all members...**\nUse /cancel to stop.")
    
    users = []
    try:
        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot and not member.user.is_deleted:
                users.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
    except Exception as e:
        TAG_ALL_PROCESSES[chat_id] = False
        return await message.reply_text(f"Error fetching members: {e}")
        
    if not users:
        TAG_ALL_PROCESSES[chat_id] = False
        return await message.reply_text("No members found to tag.")
        
    # Send mentions in batches of 5 to prevent giant spam blocks
    batch_size = 5
    for i in range(0, len(users), batch_size):
        if not TAG_ALL_PROCESSES.get(chat_id, False):
            break
            
        batch = users[i:i+batch_size]
        msg = " ".join(batch)
        if text:
            msg = f"{text}\n\n{msg}"
            
        try:
            await client.send_message(chat_id, msg)
            await asyncio.sleep(2)  # Avoid flood wait limits
        except Exception as e:
            print(f"Error in tagall: {e}")
            await asyncio.sleep(5)
            
    if TAG_ALL_PROCESSES.get(chat_id, False):
        TAG_ALL_PROCESSES[chat_id] = False
        await message.reply_text("✅ **Tagging complete!**")

@app.on_message(filters.command(["cancel", "stop"]) & filters.group)
async def cancel_tag_all(client, message: Message):
    chat_id = message.chat.id
    
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in ["creator", "administrator"]:
        return await message.reply_text("Only admins can use the /cancel command.")
        
    if chat_id in TAG_ALL_PROCESSES and TAG_ALL_PROCESSES[chat_id]:
        TAG_ALL_PROCESSES[chat_id] = False
        await message.reply_text("🛑 **Tagall process cancelled!**")
    else:
        # Check if they are trying to stop a game, because we have /stopgame
        # Just notify them if no tagall process is running
        pass
