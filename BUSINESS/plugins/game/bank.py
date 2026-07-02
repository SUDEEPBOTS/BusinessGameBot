# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message
from BUSINESS.core.bot import app
from BUSINESS.game.core import ACTIVE_GAMES, BOARD_SPACES

@app.on_message(filters.command("loan") & filters.group)
async def take_loan_command(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await message.reply_text("No active game in this chat.")
        
    game = ACTIVE_GAMES[chat_id]
    if game.status != "playing":
        return await message.reply_text("The game hasn't started yet.")
        
    player = next((p for p in game.players if p.user_id == message.from_user.id), None)
    if not player:
        return await message.reply_text("You are not in this game!")
        
    current_space = BOARD_SPACES[player.position]
    if current_space.get("action") != "bank":
        return await message.reply_text("You must be on the **Bank** tile to take a loan!")
        
    if player.loan > 0:
        return await message.reply_text(f"You already have an active loan of ${player.loan}! Use `/payloan` to clear it first.")
        
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/loan <amount>`\nMax limit: $5000")
        
    try:
        amount = int(message.command[1])
    except ValueError:
        return await message.reply_text("Please enter a valid amount.")
        
    if amount <= 0 or amount > 5000:
        return await message.reply_text("Loan amount must be between $1 and $5000.")
        
    # Grant loan
    player.loan = amount
    player.emi = int(amount * 0.1)  # 10% per turn
    if player.emi < 50:
        player.emi = 50 # Minimum EMI
        
    player.balance += amount
    
    text = f"🏦 **LOAN APPROVED!**\n\n**{player.name}** has taken a loan of **${amount}**.\n"
    text += f"📉 An EMI of **${player.emi}** will be deducted on every turn.\n"
    text += f"💰 **New Balance:** ${player.balance}"
    
    await message.reply_text(text)


@app.on_message(filters.command("payloan") & filters.group)
async def pay_loan_command(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in ACTIVE_GAMES:
        return await message.reply_text("No active game in this chat.")
        
    game = ACTIVE_GAMES[chat_id]
    player = next((p for p in game.players if p.user_id == message.from_user.id), None)
    
    if not player:
        return await message.reply_text("You are not in this game!")
        
    if player.loan <= 0:
        return await message.reply_text("You don't have any active loans.")
        
    if len(message.command) < 2:
        return await message.reply_text(f"Your current loan is **${player.loan}**.\nUsage: `/payloan <amount>` or `/payloan full`")
        
    arg = message.command[1].lower()
    if arg == "full":
        amount = player.loan
    else:
        try:
            amount = int(arg)
        except ValueError:
            return await message.reply_text("Please enter a valid amount or 'full'.")
            
    if amount <= 0:
        return await message.reply_text("Amount must be greater than 0.")
        
    if amount > player.loan:
        amount = player.loan
        
    if player.balance < amount:
        return await message.reply_text(f"You don't have enough money! Your balance: ${player.balance}")
        
    player.balance -= amount
    player.loan -= amount
    
    text = f"✅ **{player.name} paid ${amount} towards their loan!**\n"
    if player.loan <= 0:
        player.loan = 0
        player.emi = 0
        text += "🎉 **Your loan is fully cleared! No more EMIs!**"
    else:
        # Recalculate EMI
        player.emi = int(player.loan * 0.1)
        if player.emi < 50:
            player.emi = 50
        text += f"📉 **Remaining Loan:** ${player.loan}\n📉 **New EMI:** ${player.emi}/turn"
        
    await message.reply_text(text)
