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
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from BUSINESS.core.bot import app
from BUSINESS.database.db import db
from BUSINESS.game.core import ACTIVE_GAMES, BOARD_SPACES
from BUSINESS.utils.language import get_string
import time

PENDING_TRADES = {}


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

@app.on_message(filters.command("trade") & filters.group)
async def trade_command(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await message.reply_text("No active game.")
    game = ACTIVE_GAMES[chat_id]
    
    if not message.reply_to_message:
        return await message.reply_text("Please reply to the player you want to trade with.\nUsage: `/trade <property_id> <price_to_sell>`")
        
    args = message.command
    if len(args) < 3:
        return await message.reply_text("Usage: `/trade <property_id> <price_to_sell>`")
        
    try:
        prop_id = int(args[1])
        price = int(args[2])
    except ValueError:
        return await message.reply_text("Property ID and Price must be numbers.")
        
    if price < 0:
        return await message.reply_text("Price cannot be negative.")
        
    sender_id = message.from_user.id
    target_id = message.reply_to_message.from_user.id
    
    if sender_id == target_id:
        return await message.reply_text("You can't trade with yourself!")
        
    sender = next((p for p in game.players if p.user_id == sender_id), None)
    target = next((p for p in game.players if p.user_id == target_id), None)
    
    if not sender or not target:
        return await message.reply_text("Both users must be playing the game.")
        
    if prop_id not in sender.properties:
        return await message.reply_text("You don't own this property!")
        
    trade_id = f"{chat_id}_{sender_id}_{target_id}_{int(time.time())}"
    PENDING_TRADES[trade_id] = {
        "prop_id": prop_id,
        "price": price,
        "sender": sender,
        "target": target,
        "chat_id": chat_id
    }
    
    prop_name = BOARD_SPACES[prop_id]['name']
    offer_text = f"**{prop_name}** for **${price}**"
    
    text = get_string(lang, "TRADE_PROPOSAL").format(
        sender=sender.name, target=target.name, offer_text=offer_text
    )
    
    buttons = [
        [
            InlineKeyboardButton(get_string(lang, "BTN_ACCEPT"), callback_data=f"trade_accept_{trade_id}"),
            InlineKeyboardButton(get_string(lang, "BTN_DECLINE"), callback_data=f"trade_decline_{trade_id}")
        ]
    ]
    
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex(r"^trade_(accept|decline)_"))
async def trade_callback(client, callback_query):
    data = callback_query.data.split("_")
    action = data[1]
    trade_id = "_".join(data[2:])
    
    if trade_id not in PENDING_TRADES:
        return await callback_query.answer("This trade has expired or already been processed.", show_alert=True)
        
    trade = PENDING_TRADES[trade_id]
    
    if callback_query.from_user.id != trade["target"].user_id:
        return await callback_query.answer("This trade offer is not for you!", show_alert=True)
        
    chat_id = trade["chat_id"]
    if chat_id not in ACTIVE_GAMES:
        del PENDING_TRADES[trade_id]
        return await callback_query.answer("Game has ended.", show_alert=True)
        
    game = ACTIVE_GAMES[chat_id]
    sender = trade["sender"]
    target = trade["target"]
    
    # Verify players are still in game
    if sender not in game.players or target not in game.players:
        del PENDING_TRADES[trade_id]
        return await callback_query.message.edit_text("One of the players is no longer in the game.")
        
    if action == "decline":
        text = get_string(lang, "TRADE_DECLINED").format(target=target.name, sender=sender.name)
        await callback_query.message.edit_text(text)
        del PENDING_TRADES[trade_id]
        return
        
    # Accept logic
    prop_id = trade["prop_id"]
    price = trade["price"]
    
    if prop_id not in sender.properties:
        return await callback_query.answer(f"{sender.name} no longer owns this property!", show_alert=True)
        
    if target.balance < price:
        return await callback_query.answer("You don't have enough money to accept this trade!", show_alert=True)
        
    # Execute trade
    level = sender.properties.pop(prop_id)
    target.properties[prop_id] = level
    target.balance -= price
    sender.balance += price
    
    prop_name = BOARD_SPACES[prop_id]['name']
    text = get_string(lang, "TRADE_ACCEPTED").format(target=target.name, sender=sender.name)
    text += f"\n\n🏠 **{prop_name}** is now owned by **{target.name}**."
    
    await callback_query.message.edit_text(text)
    del PENDING_TRADES[trade_id]