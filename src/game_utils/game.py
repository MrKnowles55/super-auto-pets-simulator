from src.action_utils.battle import Battle
from src.team_utils.team import Team


class Game:
    def __init__(self):
        self.battle_handler = Battle(Team("Player"), Team("Enemy"))
        self.shop_handler = None
        self.team = Team("Game")

    def battle_mode(self):
        self.battle_handler.battle_loop()

    def shop_mode(self):
        pass

    def game_loop(self):
        self.shop_mode()
        self.battle_mode()
