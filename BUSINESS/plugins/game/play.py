from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from BUSINESS.core.bot import app
from BUSINESS.game.core import ACTIVE_GAMES, BOARD_SPACES
from BUSINESS.utils.fonts import button_font

@app.on_message(filters.command("roll") & filters.group)
async def roll_command(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await message.reply_text("No active game. Start one with /business")
        
    game = ACTIVE_GAMES[chat_id]
    
    if game.status != "playing":
        return await message.reply_text("The game hasn't started yet! Use /start_game.")
        
    current_player = game.get_current_player()
    
    if message.from_user.id != current_player.user_id:
        return await message.reply_text(f"It's not your turn! Waiting for {current_player.name}.")
        
    # Send the dice emoji
    dice_msg = await client.send_dice(chat_id, emoji="🎲")
    dice_value = dice_msg.dice.value
    
    # Wait for the animation to complete visually before replying
    import asyncio
    await asyncio.sleep(3)
    
    passed_start = current_player.move(dice_value)
    current_space = BOARD_SPACES[current_player.position]
    
    text = f"🎲 **{current_player.name} rolled a {dice_value}!**\n\n"
    text += f"Landed on: **{current_space['name']}**\n"
    
    if passed_start:
        text += "💰 *Passed Start! Collected $2000!*\n"
        
    buttons = []
    
    if current_space['type'] == 'property':
        if current_space['name'] in [p['name'] for p in game.players for p in getattr(p, 'properties', [])]:
            # Property is owned, pay rent logic here
            text += "🏠 This property is already owned! (Rent logic coming soon...)"
        else:
            text += f"💵 Price: ${current_space['price']}\n💸 Rent: ${current_space['rent']}"
            buttons.append([InlineKeyboardButton(text=button_font("BUY PROPERTY"), callback_data=f"buy_{current_player.position}")])
            
    elif current_space['type'] == 'tax':
        current_player.balance -= current_space['amount']
        text += f"💸 Paid ${current_space['amount']} in taxes."
        
    text += f"\n\nNext turn: **{game.players[(game.turn_index + 1) % len(game.players)].name}**"
    
    game.next_turn()
    
    if buttons:
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text(text)

@app.on_message(filters.command("board") & filters.group)
async def board_command(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await message.reply_text("No active game.")
        
    game = ACTIVE_GAMES[chat_id]
    
    board_text = "🏦 **Game Status:**\n\n"
    for p in game.players:
        pos_name = BOARD_SPACES[p.position]['name']
        board_text += f"👤 **{p.name}**\n"
        board_text += f"💵 Balance: ${p.balance}\n"
        board_text += f"📍 Position: {pos_name}\n\n"
        
    await message.reply_text(board_text)
