from src.game_utils.game import Game
from src.pet_utils.pet import Pet


class Simulator:
    def __init__(self):
        self.game_handler = Game()
        self.running = True

    def run(self):
        while self.running:
            self.sim_loop()

    def generate_teams(self):
        self.game_handler.battle_handler.player_team.pets_list = []
        self.game_handler.battle_handler.enemy_team.pets_list = []
        for _ in range(5):
            self.game_handler.battle_handler.player_team.add_pet(Pet("Pet"))
            self.game_handler.battle_handler.enemy_team.add_pet(Pet("Pet"))

    def sim_loop(self):
        self.game_handler.game_loop()

        self.running = False


if __name__ == "__main__":
    Sim = Simulator()
    Sim.generate_teams()
    Sim.run()
