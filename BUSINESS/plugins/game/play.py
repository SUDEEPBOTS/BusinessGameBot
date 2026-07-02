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
from BUSINESS.game.core import ACTIVE_GAMES, BOARD_SPACES, CHANCE_CARDS
from BUSINESS.utils.fonts import button_font
from BUSINESS.utils.language import get_string
from BUSINESS.database.db import db
import random

async def handle_bankruptcy(chat_id, game, player, lang):
    if db:
        await db.inc_user_stats(player.user_id, "bankruptcies", 1)
    game.players.remove(player)
    await app.send_message(chat_id, get_string(lang, "PLAYER_BANKRUPT").format(name=player.name))
    if len(game.players) == 1:
        winner = game.players[0]
        if db:
            await db.inc_user_stats(winner.user_id, "games_won", 1)
            await db.inc_user_stats(winner.user_id, "total_wealth_earned", winner.balance)
            for p in game.initial_players:
                await db.inc_user_stats(p.user_id, "games_played", 1)
        await app.send_message(chat_id, get_string(lang, "GAME_OVER").format(winner=winner.name, wealth=winner.balance))
        del ACTIVE_GAMES[chat_id]
        return True
    return False

@app.on_message(filters.command("roll") & filters.group)
async def roll_command(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    await message.delete()
    chat_id = message.chat.id
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
    if chat_id not in ACTIVE_GAMES:
        return await app.send_message(chat_id, get_string(lang, "NO_ACTIVE_GAME"))
    game = ACTIVE_GAMES[chat_id]
    if game.status != "playing":
        return await app.send_message(chat_id, get_string(lang, "GAME_NOT_STARTED"))
    current_player = game.get_current_player()
    if message.from_user.id != current_player.user_id:
        return await app.send_message(chat_id, get_string(lang, "NOT_YOUR_TURN").format(name=current_player.name))
    next_player_name = game.players[(game.turn_index + 1) % len(game.players)].name
    if current_player.in_jail:
        current_player.jail_turns += 1
        if current_player.jail_turns >= 3:
            current_player.in_jail = False
            current_player.jail_turns = 0
            await app.send_message(chat_id, get_string(lang, "JAIL_FREE").format(name=current_player.name, next_player=next_player_name))
            game.next_turn()
            return
        else:
            await app.send_message(chat_id, get_string(lang, "JAIL_SKIP").format(name=current_player.name, turns=current_player.jail_turns, next_player=next_player_name))
            game.next_turn()
            return
            
    # Reset AFK skips since player is active
    game.afk_skips = 0
    
    dice_msg = await client.send_dice(chat_id, emoji="🎲")
    dice_value = dice_msg.dice.value
    import asyncio
    await asyncio.sleep(3)
    
    emi_msg = ""
    if current_player.loan > 0:
        if current_player.balance < current_player.emi:
            current_player.balance = -1
        else:
            current_player.balance -= current_player.emi
            current_player.loan -= current_player.emi
            emi_msg = f"📉 Paid EMI of ${current_player.emi}. Remaining Loan: ${max(0, current_player.loan)}\n"
            if current_player.loan <= 0:
                current_player.loan = 0
                current_player.emi = 0

    passed_start = current_player.move(dice_value)
    current_space = BOARD_SPACES[current_player.position]
    text = get_string(lang, "ROLL_MSG").format(name=current_player.name, dice=dice_value, space_name=current_space['name'])
    text += emi_msg

    if passed_start:
        text += get_string(lang, "PASSED_START")
    buttons = []
    if current_space['type'] == 'property':
        owner = game.get_property_owner(current_player.position)
        if owner:
            upgrade_level = owner.properties[current_player.position]
            if owner.user_id == current_player.user_id:
                if upgrade_level < 5:
                    upgrade_cost = current_space['price'] // 2
                    text += get_string(lang, "PROP_OWNED_SELF_UPG").format(level=upgrade_level, cost=upgrade_cost)
                    buttons.append([InlineKeyboardButton(text=button_font(get_string(lang, "BTN_UPGRADE_PROPERTY")), callback_data=f"upg_{current_player.position}")])
                else:
                    text += get_string(lang, "PROP_OWNED_SELF_MAX")
            else:
                multiplier = [1, 2, 3, 4, 5, 10]
                rent = current_space['rent'] * multiplier[upgrade_level]
                if current_player.balance < rent:
                    rent = current_player.balance
                    text += get_string(lang, "BANKRUPT_MSG").format(name=current_player.name)
                current_player.balance -= rent
                owner.balance += rent
                text += get_string(lang, "RENT_PAID").format(owner=owner.name, level=upgrade_level, rent=rent)
        else:
            text += get_string(lang, "PROP_UNOWNED").format(price=current_space['price'], rent=current_space['rent'])
            buttons.append([InlineKeyboardButton(text=button_font(get_string(lang, "BTN_BUY_PROPERTY")), callback_data=f"buy_{current_player.position}")])
    elif current_space['type'] == 'tax':
        amount = current_space['amount']
        if current_player.balance < amount:
            text += get_string(lang, "BANKRUPT_MSG").format(name=current_player.name)
            current_player.balance = -1 
        else:
            current_player.balance -= amount
            text += get_string(lang, "TAX_PAID").format(amount=amount)
    elif current_space['type'] == 'chance':
        card = random.choice(CHANCE_CARDS)
        text += get_string(lang, "CHANCE_CARD_MSG").format(text=card['text'])
        if "amount" in card:
            if card['amount'] < 0 and current_player.balance < abs(card['amount']):
                text += get_string(lang, "BANKRUPT_MSG").format(name=current_player.name)
                current_player.balance = -1
            else:
                current_player.balance += card['amount']
        elif "action" in card and card["action"] == "jail":
            current_player.in_jail = True
            current_player.jail_turns = 0
            current_player.position = next(i for i, s in enumerate(BOARD_SPACES) if s.get("action") == "jail")
    elif current_space['type'] == 'special' and current_space.get('action') == 'jail':
        current_player.in_jail = True
        current_player.jail_turns = 0
        text += get_string(lang, "GO_TO_JAIL")
    elif current_space['type'] == 'special' and current_space.get('action') == 'bank':
        text += "🏦 **Bank:** You can take a loan!\nUse `/loan <amount>` (Max $5000)."
    if current_player.balance < 0:
        is_game_over = await handle_bankruptcy(chat_id, game, current_player, lang)
        if is_game_over:
            return
    next_player_name = game.players[(game.turn_index + 1) % len(game.players)].name
    text += get_string(lang, "NEXT_TURN").format(next_player=next_player_name)
    game.next_turn()
    
    from BUSINESS.utils.image_gen import generate_roll_image
    owner_name = None
    if current_space['type'] == 'property':
        prop_owner = game.get_property_owner(current_player.position)
        if prop_owner:
            owner_name = prop_owner.name

    photo_io = generate_roll_image(
        player_name=current_player.name,
        dice_val=dice_value,
        space_name=current_space['name'],
        price=current_space.get('price'),
        rent=current_space.get('rent'),
        owner=owner_name,
        balance=current_player.balance
    )
    
    if buttons:
        await app.send_photo(chat_id, photo=photo_io, caption=text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await app.send_photo(chat_id, photo=photo_io, caption=text)
    from BUSINESS.plugins.game.afk import afk_timer
    asyncio.create_task(afk_timer(chat_id, game.turn_id, next_player_name))

@app.on_message(filters.command("board") & filters.group)
async def board_command(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    await message.delete()
    chat_id = message.chat.id
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
    if chat_id not in ACTIVE_GAMES:
        return await app.send_message(chat_id, get_string(lang, "NO_ACTIVE_GAME"))
    game = ACTIVE_GAMES[chat_id]
    board_text = get_string(lang, "BOARD_TITLE")
    for p in game.players:
        pos_name = BOARD_SPACES[p.position]['name']
        board_text += get_string(lang, "BOARD_PLAYER_STAT").format(name=p.name, balance=p.balance, pos_name=pos_name)
    await app.send_message(chat_id, board_text)

@app.on_callback_query(filters.regex(r"^buy_(\d+)$"))
async def buy_property_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
    if chat_id not in ACTIVE_GAMES:
        return await callback_query.answer(get_string(lang, "NO_ACTIVE_GAME"), show_alert=True)
    game = ACTIVE_GAMES[chat_id]
    pos = int(callback_query.matches[0].group(1))
    buyer = None
    for p in game.players:
        if p.user_id == callback_query.from_user.id:
            buyer = p
            break
    if not buyer:
        return await callback_query.answer(get_string(lang, "NOT_IN_GAME"), show_alert=True)
    if buyer.position != pos:
        return await callback_query.answer(get_string(lang, "NOT_ON_PROPERTY"), show_alert=True)
    if game.get_property_owner(pos):
        return await callback_query.answer(get_string(lang, "ALREADY_OWNED"), show_alert=True)
    property_data = BOARD_SPACES[pos]
    price = property_data['price']
    if buyer.balance < price:
        return await callback_query.answer(get_string(lang, "NOT_ENOUGH_MONEY"), show_alert=True)
    buyer.balance -= price
    buyer.properties[pos] = 0
    success_msg = get_string(lang, "BUY_SUCCESS_MSG").format(name=buyer.name, prop_name=property_data['name'], price=price)
    try:
        parts = callback_query.message.text.rsplit('\n\n', 1)
        new_text = f"{parts[0]}\n{success_msg}\n\n{parts[1]}"
    except Exception:
        new_text = f"{callback_query.message.text}\n{success_msg}"
    await callback_query.message.edit_text(new_text)
    await callback_query.answer(get_string(lang, "BOUGHT_PROPERTY").format(name=property_data['name']), show_alert=True)

@app.on_callback_query(filters.regex(r"^upg_(\d+)$"))
async def upgrade_property_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
    if chat_id not in ACTIVE_GAMES:
        return await callback_query.answer(get_string(lang, "NO_ACTIVE_GAME"), show_alert=True)
    game = ACTIVE_GAMES[chat_id]
    pos = int(callback_query.matches[0].group(1))
    buyer = None
    for p in game.players:
        if p.user_id == callback_query.from_user.id:
            buyer = p
            break
    if not buyer:
        return await callback_query.answer(get_string(lang, "NOT_IN_GAME"), show_alert=True)
    if pos not in buyer.properties:
        return await callback_query.answer(get_string(lang, "DONT_OWN_PROP"), show_alert=True)
    current_level = buyer.properties[pos]
    if current_level >= 5:
        return await callback_query.answer(get_string(lang, "MAX_LEVEL_REACHED"), show_alert=True)
    property_data = BOARD_SPACES[pos]
    upgrade_cost = property_data['price'] // 2
    if buyer.balance < upgrade_cost:
        return await callback_query.answer(get_string(lang, "NOT_ENOUGH_MONEY_UPG"), show_alert=True)
    buyer.balance -= upgrade_cost
    buyer.properties[pos] += 1
    new_level = buyer.properties[pos]
    type_str = "House" if new_level < 5 else "Hotel"
    success_msg = get_string(lang, "UPG_SUCCESS_MSG").format(name=buyer.name, prop_name=property_data['name'], level=new_level, type=type_str, cost=upgrade_cost)
    try:
        parts = callback_query.message.text.rsplit('\n\n', 1)
        new_text = f"{parts[0]}\n{success_msg}\n\n{parts[1]}"
    except Exception:
        new_text = f"{callback_query.message.text}\n{success_msg}"
    await callback_query.message.edit_text(new_text)
    await callback_query.answer(get_string(lang, "UPGRADED_PROPERTY").format(level=new_level), show_alert=True)