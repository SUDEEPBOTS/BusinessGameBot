from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from BUSINESS.core.bot import app
from BUSINESS.game.core import Game, ACTIVE_GAMES
from BUSINESS.utils.fonts import button_font

@app.on_message(filters.command("business") & filters.group)
async def create_lobby(client, message: Message):
    chat_id = message.chat.id
    if chat_id in ACTIVE_GAMES:
        return await message.reply_text("A game or lobby is already active in this group! Use /join to join.")
        
    game = Game(chat_id)
    game.add_player(message.from_user.id, message.from_user.first_name)
    ACTIVE_GAMES[chat_id] = game
    
    text = f"""
🎲 **New Business Game Lobby Created!** 🏦

**Host:** {message.from_user.mention}
**Players (1/6):**
1. {message.from_user.first_name}

Type /join to enter the game. Admin/Host can type /start_game when everyone is ready.
"""
    buttons = [[InlineKeyboardButton(text=button_font("JOIN LOBBY"), callback_data="join_game")]]
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_message(filters.command("join") & filters.group)
async def join_command(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await message.reply_text("There is no active lobby. Use /business to create one.")
        
    game = ACTIVE_GAMES[chat_id]
    
    if game.status != "waiting":
        return await message.reply_text("The game has already started!")
        
    # Check if already in
    for p in game.players:
        if p.user_id == message.from_user.id:
            return await message.reply_text("You have already joined this game!")
            
    success = game.add_player(message.from_user.id, message.from_user.first_name)
    if success:
        await message.reply_text(f"{message.from_user.mention} joined the game! ({len(game.players)}/6)")
    else:
        await message.reply_text("The lobby is full! Maximum 6 players allowed.")

@app.on_message(filters.command("start_game") & filters.group)
async def start_game_command(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await message.reply_text("There is no active lobby.")
        
    game = ACTIVE_GAMES[chat_id]
    
    if game.status != "waiting":
        return await message.reply_text("The game is already running.")
        
    if len(game.players) < 2:
        return await message.reply_text("You need at least 2 players to start the game.")
        
    # Only Host or Admin can start. Let's simplify: if it's the host.
    if message.from_user.id != game.players[0].user_id:
        return await message.reply_text("Only the host who created the lobby can start the game.")
        
    game.status = "playing"
    
    player_names = "\n".join([f"{i+1}. {p.name}" for i, p in enumerate(game.players)])
    
    start_msg = f"""
🚀 **THE GAME HAS STARTED!** 🚀

Each player starts with **$5000**.
It's {game.players[0].name}'s turn!

**Players:**
{player_names}

Type /roll to throw the dice! 🎲
"""
    await message.reply_text(start_msg)

@app.on_callback_query(filters.regex("^join_game$"))
async def join_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await callback_query.answer("No active lobby here.", show_alert=True)
        
    game = ACTIVE_GAMES[chat_id]
    
    if game.status != "waiting":
        return await callback_query.answer("The game has already started!", show_alert=True)
        
    for p in game.players:
        if p.user_id == callback_query.from_user.id:
            return await callback_query.answer("You are already in the lobby!", show_alert=True)
            
    success = game.add_player(callback_query.from_user.id, callback_query.from_user.first_name)
    if success:
        player_list = "\n".join([f"{i+1}. {p.name}" for i, p in enumerate(game.players)])
        text = f"🎲 **New Business Game Lobby Created!** 🏦\n\n**Host:** {game.players[0].name}\n**Players ({len(game.players)}/6):**\n{player_list}\n\nType /join to enter the game. Admin/Host can type /start_game when everyone is ready."
        await callback_query.message.edit_text(text, reply_markup=callback_query.message.reply_markup)
        await callback_query.answer("Joined the lobby successfully!", show_alert=True)
    else:
        await callback_query.answer("The lobby is full!", show_alert=True)
