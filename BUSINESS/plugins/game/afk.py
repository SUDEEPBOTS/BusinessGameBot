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

import asyncio
from BUSINESS.core.bot import app
from BUSINESS.database.db import db
from BUSINESS.game.core import ACTIVE_GAMES
from BUSINESS.utils.language import get_string

async def afk_timer(chat_id: int, expected_turn_id: int, player_name: str):
    await asyncio.sleep(60) 
    if chat_id not in ACTIVE_GAMES:
        return
    game = ACTIVE_GAMES[chat_id]
    if game.status != "playing":
        return
    if game.turn_id == expected_turn_id:
        if not hasattr(game, "afk_skips"):
            game.afk_skips = 0
        game.afk_skips += 1
        
        if game.afk_skips >= 2:
            await app.send_message(chat_id, "🛑 **The game has been automatically cancelled because players are AFK.**")
            if chat_id in ACTIVE_GAMES:
                del ACTIVE_GAMES[chat_id]
            return

        lang = await db.get_group_lang(chat_id) if "chat_id" in locals() else (await db.get_group_lang(message.chat.id) if "message" in locals() else (await db.get_group_lang(callback_query.message.chat.id) if "callback_query" in locals() else "en"))
        game.next_turn()
        next_player = game.get_current_player()
        if not next_player:
            return
        await app.send_message(chat_id, get_string(lang, "AFK_SKIPPED").format(
            name=player_name, 
            next_player=next_player.name
        ))
        asyncio.create_task(afk_timer(chat_id, game.turn_id, next_player.name))