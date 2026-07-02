# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from BUSINESS.core.bot import app
from BUSINESS.database.db import db
from BUSINESS.plugins.partygame.core import PartyGameSession, ACTIVE_PARTY_GAMES
from BUSINESS.utils.fonts import button_font

@app.on_message(filters.command("party") & filters.group)
async def party_create_lobby(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    chat_id = message.chat.id
    if chat_id in ACTIVE_PARTY_GAMES:
        return await app.send_message(message.chat.id, "A Party Game is already active or waiting in this group! Use /partyjoin.")
        
    game = PartyGameSession(chat_id)
    game.add_player(message.from_user.id, message.from_user.first_name)
    ACTIVE_PARTY_GAMES[chat_id] = game
    
    buttons = [[InlineKeyboardButton(text=button_font("JOIN PARTY"), callback_data="join_party_game")]]
    text = f"🎭 **New Party Game Lobby!** 🎲\n\nHost: {message.from_user.mention}\n\n**Players (1/5):**\n1. {message.from_user.first_name}\n\nClick the button or use `/partyjoin`."
    
    await app.send_message(message.chat.id, text, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_message(filters.command("partyjoin") & filters.group)
async def party_join_cmd(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    chat_id = message.chat.id
    if chat_id not in ACTIVE_PARTY_GAMES:
        return await app.send_message(message.chat.id, "No active Party Game lobby.")
    
    game = ACTIVE_PARTY_GAMES[chat_id]
    if game.status != "waiting":
        return await app.send_message(message.chat.id, "The game has already started!")
        
    for p in game.players:
        if p.user_id == message.from_user.id:
            return await app.send_message(message.chat.id, "You are already in this game!")
            
    if game.add_player(message.from_user.id, message.from_user.first_name):
        await app.send_message(message.chat.id, f"✅ {message.from_user.mention} joined the Party Game! ({len(game.players)}/5)")
    else:
        await app.send_message(message.chat.id, "Lobby is full! Maximum 5 players allowed.")

@app.on_callback_query(filters.regex("^join_party_game$"))
async def party_join_cb(client, callback_query):
    chat_id = callback_query.message.chat.id
    if chat_id not in ACTIVE_PARTY_GAMES:
        return await callback_query.answer("No active Party Game lobby.", show_alert=True)
        
    game = ACTIVE_PARTY_GAMES[chat_id]
    if game.status != "waiting":
        return await callback_query.answer("The game has already started!", show_alert=True)
        
    for p in game.players:
        if p.user_id == callback_query.from_user.id:
            return await callback_query.answer("You are already in this game!", show_alert=True)
            
    if game.add_player(callback_query.from_user.id, callback_query.from_user.first_name):
        player_list = "\n".join([f"{i+1}. {p.name}" for i, p in enumerate(game.players)])
        text = f"🎭 **New Party Game Lobby!** 🎲\n\nHost: {game.players[0].name}\n\n**Players ({len(game.players)}/5):**\n{player_list}\n\nWhen ready, the host can send `/partystart`."
        await callback_query.message.edit_text(text, reply_markup=callback_query.message.reply_markup)
        await callback_query.answer("Joined successfully!", show_alert=True)
    else:
        await callback_query.answer("Lobby is full! Maximum 5 players allowed.", show_alert=True)
