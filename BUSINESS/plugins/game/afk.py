import asyncio
from BUSINESS.core.bot import app
from BUSINESS.game.core import ACTIVE_GAMES
from BUSINESS.utils.language import get_string

async def afk_timer(chat_id: int, expected_turn_id: int, player_name: str):
    await asyncio.sleep(60) # 60 seconds to roll
    
    # Check if game still exists and turn hasn't changed
    if chat_id not in ACTIVE_GAMES:
        return
        
    game = ACTIVE_GAMES[chat_id]
    if game.status != "playing":
        return
        
    if game.turn_id == expected_turn_id:
        # Turn hasn't changed, skip player
        lang = "en"
        game.next_turn()
        
        next_player = game.get_current_player()
        if not next_player:
            return
            
        await app.send_message(chat_id, get_string(lang, "AFK_SKIPPED").format(
            name=player_name, 
            next_player=next_player.name
        ))
        
        # Start timer for the next player automatically
        asyncio.create_task(afk_timer(chat_id, game.turn_id, next_player.name))
