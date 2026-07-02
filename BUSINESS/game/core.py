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



BOARD_SPACES = [
    {"id": 0, "name": "Start", "type": "special", "action": "collect_2000"},
    {"id": 1, "name": "Mumbai", "type": "property", "price": 800, "rent": 80},
    {"id": 2, "name": "Waterways", "type": "transport", "price": 1500, "rent": 200},
    {"id": 3, "name": "Ahmedabad", "type": "property", "price": 1200, "rent": 120},
    {"id": 4, "name": "Income Tax", "type": "tax", "amount": 250},
    {"id": 5, "name": "Indore", "type": "property", "price": 1500, "rent": 150},
    {"id": 6, "name": "Chance", "type": "chance"},
    {"id": 7, "name": "Jaipur", "type": "property", "price": 2000, "rent": 200},
    {"id": 8, "name": "Jail", "type": "special", "action": "jail"},
    {"id": 9, "name": "New Delhi", "type": "property", "price": 2500, "rent": 250},
    {"id": 10, "name": "Chandigarh", "type": "property", "price": 2500, "rent": 250},
    {"id": 11, "name": "Airways", "type": "transport", "price": 2000, "rent": 250},
    {"id": 12, "name": "UNO", "type": "chance"},
    {"id": 13, "name": "Shimla", "type": "property", "price": 2800, "rent": 280},
    {"id": 14, "name": "Amritsar", "type": "property", "price": 3000, "rent": 300},
    {"id": 15, "name": "Community Chest", "type": "chance"},
    {"id": 16, "name": "Srinagar", "type": "property", "price": 3200, "rent": 320},
    {"id": 17, "name": "Bank", "type": "special", "action": "bank"},
    {"id": 18, "name": "Agra", "type": "property", "price": 3500, "rent": 350},
    {"id": 19, "name": "Kanpur", "type": "property", "price": 4000, "rent": 400},
    {"id": 20, "name": "Railways", "type": "transport", "price": 2500, "rent": 300},
    {"id": 21, "name": "Patna", "type": "property", "price": 4200, "rent": 420},
    {"id": 22, "name": "Chance", "type": "chance"},
    {"id": 23, "name": "Darjeeling", "type": "property", "price": 4500, "rent": 450},
    {"id": 24, "name": "Kolkata", "type": "property", "price": 5000, "rent": 500},
    {"id": 25, "name": "Wealth Tax", "type": "tax", "amount": 400},
    {"id": 26, "name": "Hyderabad", "type": "property", "price": 5500, "rent": 550},
    {"id": 27, "name": "Chennai", "type": "property", "price": 6000, "rent": 600},
    {"id": 28, "name": "Roadways", "type": "transport", "price": 3000, "rent": 350},
    {"id": 29, "name": "Bengaluru", "type": "property", "price": 6500, "rent": 650},
    {"id": 30, "name": "UNO", "type": "chance"},
    {"id": 31, "name": "Pune", "type": "property", "price": 7000, "rent": 700},
    {"id": 32, "name": "Goa", "type": "property", "price": 7500, "rent": 750},
    {"id": 33, "name": "Resort", "type": "special", "action": "nothing"},
    {"id": 34, "name": "Dubai", "type": "property", "price": 8500, "rent": 850},
    {"id": 35, "name": "London", "type": "property", "price": 9000, "rent": 900},
]

CHANCE_CARDS = [
    {"text": "Win a Beauty Contest! Collect $500", "amount": 500},
    {"text": "Speeding Ticket! Pay $200", "amount": -200},
    {"text": "Bank Error in your favor! Collect $1000", "amount": 1000},
    {"text": "Pay hospital bills! Pay $300", "amount": -300},
    {"text": "Go to Jail! Move directly to Jail.", "action": "jail"},
    {"text": "Inherit $800!", "amount": 800}
]

class Player:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self.balance = 5000
        self.position = 0
        self.properties = {} 
        self.in_jail = False
        self.jail_turns = 0
        self.loan = 0
        self.emi = 0

    def roll_dice(self):
        import random
        return random.randint(1, 6), random.randint(1, 6)
    def move(self, steps: int):
        old_pos = self.position
        self.position = (self.position + steps) % len(BOARD_SPACES)
        if self.position < old_pos:
            self.balance += 2000 
            return True 
        return False

class Game:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.players = []
        self.initial_players = []
        self.turn_index = 0
        self.turn_id = 0 
        self.status = "waiting" 

    def add_player(self, user_id: int, name: str):
        if len(self.players) < 6 and self.status == "waiting":
            p = Player(user_id, name)
            self.players.append(p)
            self.initial_players.append(p)
            return True
        return False

    def get_current_player(self) -> Player:
        if self.players:
            return self.players[self.turn_index]
        return None

    def next_turn(self):
        self.turn_index = (self.turn_index + 1) % len(self.players)
        self.turn_id += 1

    def get_property_owner(self, position: int) -> Player:
        for player in self.players:
            if position in player.properties:
                return player
        return None

ACTIVE_GAMES = {} 