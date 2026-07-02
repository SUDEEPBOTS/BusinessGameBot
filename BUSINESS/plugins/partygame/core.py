# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.

class PartyPlayer:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self.pos = 0
        self.balance = 5000
        
class PartyGameSession:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.players = []
        self.status = "waiting" # waiting, playing, finished
        self.turn_index = 0
        self.turn_id = 0
        self.board_length = 30 # Default boxes to finish
        
    def add_player(self, user_id: int, name: str) -> bool:
        if len(self.players) >= 5:
            return False
        self.players.append(PartyPlayer(user_id, name))
        return True

# Dictionary to hold active party games per group
ACTIVE_PARTY_GAMES = {}
