from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from BUSINESS.core.bot import app
from BUSINESS.game.core import Game, ACTIVE_GAMES
from BUSINESS.utils.fonts import button_font
from BUSINESS.utils.language import get_string
from BUSINESS.database.db import db

@app.on_message(filters.command("business") & filters.group)
async def create_lobby(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    lang = "en"
    if chat_id in ACTIVE_GAMES:
        return await app.send_message(chat_id, get_string(lang, "LOBBY_ACTIVE"))
    game = Game(chat_id)
    game.add_player(message.from_user.id, message.from_user.first_name)
    ACTIVE_GAMES[chat_id] = game
    if db:
        await db.get_user(message.from_user.id, message.from_user.first_name)
        await db.add_group(chat_id)
    text = get_string(lang, "LOBBY_CREATED").format(
        host=message.from_user.mention,
        count=1,
        players=f"1. {message.from_user.first_name}"
    )
    buttons = [[InlineKeyboardButton(text=button_font(get_string(lang, "BTN_JOIN_LOBBY")), callback_data="join_game")]]
    await app.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_message(filters.command("join") & filters.group)
async def join_command(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    lang = "en"
    if chat_id not in ACTIVE_GAMES:
        return await app.send_message(chat_id, get_string(lang, "NO_LOBBY"))
    game = ACTIVE_GAMES[chat_id]
    if game.status != "waiting":
        return await app.send_message(chat_id, get_string(lang, "GAME_ALREADY_STARTED"))
    for p in game.players:
        if p.user_id == message.from_user.id:
            return await app.send_message(chat_id, get_string(lang, "ALREADY_JOINED"))
    success = game.add_player(message.from_user.id, message.from_user.first_name)
    if success:
        if db:
            await db.get_user(message.from_user.id, message.from_user.first_name)
        await app.send_message(chat_id, get_string(lang, "PLAYER_JOINED").format(mention=message.from_user.mention, count=len(game.players)))
    else:
        await app.send_message(chat_id, get_string(lang, "LOBBY_FULL"))

from BUSINESS.plugins.game.afk import afk_timer
import asyncio

@app.on_message(filters.command("start_game") & filters.group)
async def start_game_command(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    lang = "en"
    if chat_id not in ACTIVE_GAMES:
        return await app.send_message(chat_id, get_string(lang, "NO_LOBBY"))
    game = ACTIVE_GAMES[chat_id]
    if game.status != "waiting":
        return await app.send_message(chat_id, get_string(lang, "GAME_ALREADY_STARTED"))
    if len(game.players) < 2:
        return await app.send_message(chat_id, get_string(lang, "NOT_ENOUGH_PLAYERS"))
    if message.from_user.id != game.players[0].user_id:
        return await app.send_message(chat_id, get_string(lang, "ONLY_HOST_STARTS"))
    game.status = "playing"
    player_names = "\n".join([f"{i+1}. {p.name}" for i, p in enumerate(game.players)])
    start_msg = get_string(lang, "GAME_STARTED").format(
        turn_player=game.players[0].name,
        players=player_names
    )
    await app.send_message(chat_id, start_msg)
    asyncio.create_task(afk_timer(chat_id, game.turn_id, game.players[0].name))

@app.on_callback_query(filters.regex("^join_game$"))
async def join_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    lang = "en"
    if chat_id not in ACTIVE_GAMES:
        return await callback_query.answer(get_string(lang, "NO_LOBBY"), show_alert=True)
    game = ACTIVE_GAMES[chat_id]
    if game.status != "waiting":
        return await callback_query.answer(get_string(lang, "GAME_ALREADY_STARTED"), show_alert=True)
    for p in game.players:
        if p.user_id == callback_query.from_user.id:
            return await callback_query.answer(get_string(lang, "ALREADY_JOINED"), show_alert=True)
    success = game.add_player(callback_query.from_user.id, callback_query.from_user.first_name)
    if success:
        if db:
            await db.get_user(callback_query.from_user.id, callback_query.from_user.first_name)
        player_list = "\n".join([f"{i+1}. {p.name}" for i, p in enumerate(game.players)])
        text = get_string(lang, "LOBBY_CREATED").format(
            host=game.players[0].name,
            count=len(game.players),
            players=player_list
        )
        await callback_query.message.edit_text(text, reply_markup=callback_query.message.reply_markup)
        await callback_query.answer("Joined successfully!", show_alert=True)
    else:
        await callback_query.answer(get_string(lang, "LOBBY_FULL"), show_alert=True)