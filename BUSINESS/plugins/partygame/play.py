# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message
from BUSINESS.core.bot import app
from BUSINESS.plugins.partygame.core import ACTIVE_PARTY_GAMES
import random

@app.on_message(filters.command("partystart") & filters.group)
async def party_start_cmd(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in ACTIVE_PARTY_GAMES:
        return await message.reply_text("No active Party Game lobby. Use /party first.")
        
    game = ACTIVE_PARTY_GAMES[chat_id]
    if game.status != "waiting":
        return await message.reply_text("The game has already started!")
        
    if len(game.players) < 2:
        return await message.reply_text("You need at least 2 players to start.")
        
    if message.from_user.id != game.players[0].user_id:
        return await message.reply_text("Only the host can start the game.")
        
    game.status = "playing"
    game.turn_index = 0
    current_player = game.players[0]
    
    text = f"🎭 **PARTY GAME STARTED!** 🚀\n\nWelcome to the board! Everyone starts with $5000.\nTarget: Reach Box 30!\n\n**{current_player.name}**, it is your turn!\n👉 Go to my DM and send `/proll <1-9>` to move!"
    await message.reply_text(text)

@app.on_message(filters.command(["proll", "partyroll"]))
async def party_roll_cmd(client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    is_private = message.chat.id == message.from_user.id
    
    if not is_private:
        try:
            await message.delete()
        except:
            pass
            
    active_game = None
    if not is_private:
        if chat_id in ACTIVE_PARTY_GAMES:
            game = ACTIVE_PARTY_GAMES[chat_id]
            if game.status == "playing":
                current_player = game.players[game.turn_index]
                if current_player.user_id == user_id:
                    active_game = game
                else:
                    return await app.send_message(chat_id, f"It's not your turn! Waiting for {current_player.name}.")
            else:
                return await app.send_message(chat_id, "The game has not started yet!")
        else:
            return await app.send_message(chat_id, "No active Party Game in this group.")
    else:
        for cid, game in ACTIVE_PARTY_GAMES.items():
            if game.status == "playing":
                current_player = game.players[game.turn_index]
                if current_player.user_id == user_id:
                    active_game = game
                    break
        if not active_game:
            return await message.reply_text("It is not your turn in any active Party Game, or you are not in one.")
            
    if len(message.command) < 2:
        error_msg = "Please provide a number from 1 to 9. Example: `/proll 5`"
        if is_private: return await message.reply_text(error_msg)
        else: return await app.send_message(chat_id, f"{message.from_user.mention}, {error_msg}")
        
    try:
        roll_val = int(message.command[1])
        if roll_val < 1 or roll_val > 9:
            raise ValueError
    except ValueError:
        error_msg = "Please enter a valid number between 1 and 9."
        if is_private: return await message.reply_text(error_msg)
        else: return await app.send_message(chat_id, f"{message.from_user.mention}, {error_msg}")
        
    current_player = active_game.players[active_game.turn_index]
    current_player.pos += roll_val
    
    event_text = ""
    if current_player.pos >= active_game.board_length:
        current_player.pos = active_game.board_length
        event_text = f"🎉 **{current_player.name} REACHED THE FINISH LINE!**"
        active_game.status = "finished"
    else:
        events = [
            ("Paid EMI", -500),
            ("Found a wallet", 1000),
            ("Truth or Dare Time!", 0),
            ("Mini Game Challenge! (Flappy Bird)", 0),
            ("Safe Zone", 0)
        ]
        ev = random.choice(events)
        current_player.balance += ev[1]
        
        event_text = f"📍 Landed on Box {current_player.pos}!\n"
        event_text += f"⚡ **Event:** {ev[0]}\n"
        if ev[1] != 0:
            event_text += f"💰 **Balance Change:** {'+' if ev[1] > 0 else ''}{ev[1]} (New Balance: ${current_player.balance})"
            
    group_msg = f"🎲 **{current_player.name} secretly rolled the dice!**\n\n{event_text}"
    
    if active_game.status == "finished":
        winner = max(active_game.players, key=lambda x: x.balance)
        group_msg += f"\n\n🏆 **GAME OVER!**\nWinner: {winner.name} with ${winner.balance}"
        del ACTIVE_PARTY_GAMES[active_game.chat_id]
    else:
        active_game.turn_index = (active_game.turn_index + 1) % len(active_game.players)
        next_player = active_game.players[active_game.turn_index]
        group_msg += f"\n\n👉 **Next Turn:** {next_player.name} (Use `/proll <1-9>` in group or DM)"
        
    await app.send_message(active_game.chat_id, group_msg)
    if is_private:
        await message.reply_text(f"✅ Move sent to the group! You landed on Box {current_player.pos}.")
