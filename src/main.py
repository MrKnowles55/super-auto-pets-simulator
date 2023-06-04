from src.game_utils.game import Game
from src.pet_utils.pet import Pet
from src.data_utils.pool import get_pack


class Simulator:
    def __init__(self, game_mode, sims_to_run=3, pet_pack="Turtle"):
        self.game_handler = None
        self.running = True
        self.sims_to_run = sims_to_run
        self.pet_pack = get_pack(pet_pack)
        self.game_mode = game_mode

    def setup(self):
        # Login
        # Pick Pack
        # Pick Game Mode
        # Load Settings
        self.create_game()

    def create_game(self):
        # Create Game
        # Load Pack Data
        # Load Game Mode
        # Load Other Settings
        self.game_handler = Game(pack=self.pet_pack, game_mode=self.game_mode)

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
        sim_count = 0
        while sim_count < self.sims_to_run:
            self.setup()
            lives = self.game_handler.lives
            score = 0
            player_pets = []
            while lives > 0 and score < 10:
                lives, score, player_pets = self.game_handler.game_loop()
            sim_count += 1
            print(f"Game {sim_count} Outcome: {lives} <3 , {score} W , {player_pets}")
        self.running = False


if __name__ == "__main__":
    Sim = Simulator(game_mode="Test")
    Sim.run()
