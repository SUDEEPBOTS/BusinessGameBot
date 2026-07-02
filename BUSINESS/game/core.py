# Core definitions for the Business Game

BOARD_SPACES = [
    {"id": 0, "name": "Start", "type": "special", "action": "collect_2000"},
    {"id": 1, "name": "Mumbai", "type": "property", "price": 1000, "rent": 100},
    {"id": 2, "name": "Waterways", "type": "transport", "price": 1500, "rent": 200},
    {"id": 3, "name": "Ahmedabad", "type": "property", "price": 1200, "rent": 120},
    {"id": 4, "name": "Income Tax", "type": "tax", "amount": 250},
    {"id": 5, "name": "Delhi", "type": "property", "price": 1500, "rent": 150},
    {"id": 6, "name": "Chance", "type": "chance"},
    {"id": 7, "name": "Chandigarh", "type": "property", "price": 2000, "rent": 200},
    {"id": 8, "name": "Jail", "type": "special", "action": "jail"},
    {"id": 9, "name": "Paris", "type": "property", "price": 2500, "rent": 250},
    {"id": 10, "name": "Wealth Tax", "type": "tax", "amount": 300},
    {"id": 11, "name": "London", "type": "property", "price": 3000, "rent": 300},
    {"id": 12, "name": "UNO", "type": "chance"}
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
        self.properties = {} # position (int) -> upgrade_level (int, 0=base, 1-4=houses, 5=hotel)
        self.in_jail = False
        self.jail_turns = 0

    def roll_dice(self):
        import random
        return random.randint(1, 6), random.randint(1, 6)
    
    def move(self, steps: int):
        old_pos = self.position
        self.position = (self.position + steps) % len(BOARD_SPACES)
        if self.position < old_pos:
            self.balance += 2000 # Passed Start
            return True # Indicates passed start
        return False

class Game:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.players = []
        self.initial_players = []
        self.turn_index = 0
        self.turn_id = 0 # Incremented each turn, helps cancel old timers
        self.status = "waiting" # waiting, playing, finished

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

ACTIVE_GAMES = {} # chat_id -> Game object
