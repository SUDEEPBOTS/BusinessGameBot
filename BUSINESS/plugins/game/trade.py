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

from pyrogram import filters
from pyrogram.types import Message
from BUSINESS.core.bot import app
from BUSINESS.game.core import ACTIVE_GAMES, BOARD_SPACES
from BUSINESS.utils.language import get_string

@app.on_message(filters.command(["properties", "myprops"]) & filters.group)
async def properties_command(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await message.reply_text("No active game in this chat.")
    game = ACTIVE_GAMES[chat_id]
    player = None
    for p in game.players:
        if p.user_id == message.from_user.id:
            player = p
            break
    if not player:
        return await message.reply_text("You are not playing in this game!")
    if not player.properties:
        return await message.reply_text("You don't own any properties.")
    text = f"🏠 **{player.name}'s Properties:**\n\n"
    for pos, level in player.properties.items():
        prop = BOARD_SPACES[pos]
        type_str = "Hotel" if level == 5 else f"Level {level}"
        sell_value = prop['price'] // 2
        text += f"🔹 **ID {pos}:** {prop['name']} ({type_str}) - Sell Value: ${sell_value}\n"
    text += "\nTo sell a property back to the bank for half price, use `/sell <ID>`"
    await message.reply_text(text)

@app.on_message(filters.command("sell") & filters.group)
async def sell_command(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await message.reply_text("No active game in this chat.")
    game = ACTIVE_GAMES[chat_id]
    if len(message.command) < 2:
        return await message.reply_text("Please provide a property ID. Usage: `/sell <ID>`\nUse `/properties` to see IDs.")
    try:
        pos = int(message.command[1])
    except ValueError:
        return await message.reply_text("Invalid property ID. Must be a number.")
    player = None
    for p in game.players:
        if p.user_id == message.from_user.id:
            player = p
            break
    if not player:
        return await message.reply_text("You are not playing in this game!")
    if pos not in player.properties:
        return await message.reply_text("You don't own this property!")
    prop = BOARD_SPACES[pos]
    sell_value = prop['price'] // 2
    del player.properties[pos]
    player.balance += sell_value
    await message.reply_text(f"✅ **{player.name} sold {prop['name']} back to the bank for ${sell_value}!**\nNew Balance: ${player.balance}")