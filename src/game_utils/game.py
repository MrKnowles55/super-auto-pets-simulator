from src.action_utils.battle import Battle
from src.team_utils.team import Team


class Game:
    def __init__(self):
        self.battle_handler = Battle(Team("Player"), Team("Enemy"))
        self.shop_handler = None
        self.team = Team("Game")

    def battle(self):
        self.battle_handler.battle_loop()
