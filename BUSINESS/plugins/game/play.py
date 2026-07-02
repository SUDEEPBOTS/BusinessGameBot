from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from BUSINESS.core.bot import app
from BUSINESS.game.core import ACTIVE_GAMES, BOARD_SPACES, CHANCE_CARDS
from BUSINESS.utils.fonts import button_font
import random

@app.on_message(filters.command("roll") & filters.group)
async def roll_command(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await app.send_message(chat_id, "No active game. Start one with /business")
        
    game = ACTIVE_GAMES[chat_id]
    
    if game.status != "playing":
        return await app.send_message(chat_id, "The game hasn't started yet! Use /start_game.")
        
    current_player = game.get_current_player()
    
    if message.from_user.id != current_player.user_id:
        return await app.send_message(chat_id, f"It's not your turn! Waiting for {current_player.name}.")
        
    if current_player.in_jail:
        current_player.jail_turns += 1
        if current_player.jail_turns >= 3:
            current_player.in_jail = False
            current_player.jail_turns = 0
            await app.send_message(chat_id, f"🚓 **{current_player.name}** served their sentence and is free from Jail!\n\nNext turn: **{game.players[(game.turn_index + 1) % len(game.players)].name}**")
            game.next_turn()
            return
        else:
            await app.send_message(chat_id, f"🚓 **{current_player.name}** is in Jail (Turn {current_player.jail_turns}/3). Skipping turn!\n\nNext turn: **{game.players[(game.turn_index + 1) % len(game.players)].name}**")
            game.next_turn()
            return
            
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
        owner = game.get_property_owner(current_player.position)
        if owner:
            upgrade_level = owner.properties[current_player.position]
            if owner.user_id == current_player.user_id:
                if upgrade_level < 5:
                    upgrade_cost = current_space['price'] // 2
                    text += f"🏠 You own this property (Level {upgrade_level}).\nUpgrade cost: ${upgrade_cost}"
                    buttons.append([InlineKeyboardButton(text=button_font("UPGRADE PROPERTY"), callback_data=f"upg_{current_player.position}")])
                else:
                    text += "🏨 You own this property. It is fully upgraded to a Hotel!"
            else:
                multiplier = [1, 2, 3, 4, 5, 10]
                rent = current_space['rent'] * multiplier[upgrade_level]
                if current_player.balance < rent:
                    rent = current_player.balance
                    text += f"⚠️ {current_player.name} went bankrupt!\n"
                current_player.balance -= rent
                owner.balance += rent
                text += f"🏠 Owned by {owner.name} (Level {upgrade_level})!\n💸 **Paid ${rent} in rent!**"
        else:
            text += f"💵 Price: ${current_space['price']}\n💸 Base Rent: ${current_space['rent']}"
            buttons.append([InlineKeyboardButton(text=button_font("BUY PROPERTY"), callback_data=f"buy_{current_player.position}")])
            
    elif current_space['type'] == 'tax':
        current_player.balance -= current_space['amount']
        text += f"💸 Paid ${current_space['amount']} in taxes."
        
    elif current_space['type'] == 'chance':
        card = random.choice(CHANCE_CARDS)
        text += f"🃏 **CHANCE CARD:**\n*{card['text']}*\n"
        if "amount" in card:
            current_player.balance += card['amount']
        elif "action" in card and card["action"] == "jail":
            current_player.in_jail = True
            current_player.jail_turns = 0
            current_player.position = next(i for i, s in enumerate(BOARD_SPACES) if s.get("action") == "jail")
            
    elif current_space['type'] == 'special' and current_space.get('action') == 'jail':
        current_player.in_jail = True
        current_player.jail_turns = 0
        text += "🚓 **GO TO JAIL!** You are arrested."
        
    text += f"\n\nNext turn: **{game.players[(game.turn_index + 1) % len(game.players)].name}**"
    
    game.next_turn()
    
    if buttons:
        await app.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await app.send_message(chat_id, text)

@app.on_message(filters.command("board") & filters.group)
async def board_command(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await app.send_message(chat_id, "No active game.")
        
    game = ACTIVE_GAMES[chat_id]
    
    board_text = "🏦 **Game Status:**\n\n"
    for p in game.players:
        pos_name = BOARD_SPACES[p.position]['name']
        board_text += f"👤 **{p.name}**\n"
        board_text += f"💵 Balance: ${p.balance}\n"
        board_text += f"📍 Position: {pos_name}\n\n"
        
    await app.send_message(chat_id, board_text)

@app.on_callback_query(filters.regex(r"^buy_(\d+)$"))
async def buy_property_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await callback_query.answer("No active game.", show_alert=True)
        
    game = ACTIVE_GAMES[chat_id]
    pos = int(callback_query.matches[0].group(1))
    
    # Check if the player clicking is the current player
    # Actually, the button is attached to the dice roll. Only the person who rolled should be able to buy it.
    # Since turn might have already changed in roll_command, we need to check if the player is at this position.
    buyer = None
    for p in game.players:
        if p.user_id == callback_query.from_user.id:
            buyer = p
            break
            
    if not buyer:
        return await callback_query.answer("You are not in this game!", show_alert=True)
        
    if buyer.position != pos:
        return await callback_query.answer("You are not on this property!", show_alert=True)
        
    if game.get_property_owner(pos):
        return await callback_query.answer("This property is already owned!", show_alert=True)
        
    property_data = BOARD_SPACES[pos]
    price = property_data['price']
    
    if buyer.balance < price:
        return await callback_query.answer("You don't have enough money!", show_alert=True)
        
    buyer.balance -= price
    buyer.properties[pos] = 0
    
    await callback_query.message.edit_text(
        f"{callback_query.message.text.split('Next turn:')[0]}\n✅ **{buyer.name} bought {property_data['name']} for ${price}!**\n\nNext turn:{callback_query.message.text.split('Next turn:')[1]}"
    )
    await callback_query.answer(f"Successfully bought {property_data['name']}!", show_alert=True)

@app.on_callback_query(filters.regex(r"^upg_(\d+)$"))
async def upgrade_property_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await callback_query.answer("No active game.", show_alert=True)
        
    game = ACTIVE_GAMES[chat_id]
    pos = int(callback_query.matches[0].group(1))
    
    buyer = None
    for p in game.players:
        if p.user_id == callback_query.from_user.id:
            buyer = p
            break
            
    if not buyer:
        return await callback_query.answer("You are not in this game!", show_alert=True)
        
    if pos not in buyer.properties:
        return await callback_query.answer("You don't own this property!", show_alert=True)
        
    current_level = buyer.properties[pos]
    if current_level >= 5:
        return await callback_query.answer("Already at max level (Hotel)!", show_alert=True)
        
    property_data = BOARD_SPACES[pos]
    upgrade_cost = property_data['price'] // 2
    
    if buyer.balance < upgrade_cost:
        return await callback_query.answer("You don't have enough money to upgrade!", show_alert=True)
        
    buyer.balance -= upgrade_cost
    buyer.properties[pos] += 1
    
    new_level = buyer.properties[pos]
    type_str = "House" if new_level < 5 else "Hotel"
    
    await callback_query.message.edit_text(
        f"{callback_query.message.text.split('Next turn:')[0]}\n✅ **{buyer.name} upgraded {property_data['name']} to Level {new_level} ({type_str}) for ${upgrade_cost}!**\n\nNext turn:{callback_query.message.text.split('Next turn:')[1]}"
    )
    await callback_query.answer(f"Successfully upgraded to Level {new_level}!", show_alert=True)
