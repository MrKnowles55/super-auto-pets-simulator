from src.action_utils.battle import Battle
from src.team_utils.team import Team
from src.pet_utils.pet import Pet


class Game:
    def __init__(self, pack, game_mode="Normal"):
        self.pack = pack
        self.game_mode = game_mode
        self.battle_handler = Battle(Team("Player"), Team("Enemy"))
        self.shop_handler = None
        # self.team = Team("Game")
        self.lives = 5
        self.score = 0
        self.turn = 0
        self.tier = 0

    # Battle

    def battle_mode(self):
        self.battle_handler.enemy_team = self.generate_team()
        results = self.battle_handler.battle_loop()
        return results

    # Shop
    def shop_mode(self):
        if self.game_mode == "Test":
            self.battle_handler.player_team = self.pack.generate_team(action_handler=self.battle_handler, team_name="Player")

    # Main Loop
    def game_loop(self):
        while self.lives > 0 and self.score < 10:
            self.turn += 1
            if self.turn in [1, 3, 5, 7, 9, 11]:
                self.tier += 1
            self.shop_mode()
            results = self.battle_mode()
            match results:
                case 1:
                    self.score += 1
                case -1:
                    self.lives -= 1
                case _:
                    pass
            # if self.game_mode == "Test":
            #     self.lives = 0

        return self.lives, self.score, self.battle_handler.player_team.pets_list

    # Utilities
    def generate_team(self, name="Enemy"):
        return self.pack.get_turn_1_team(self.battle_handler, team_name=name)
