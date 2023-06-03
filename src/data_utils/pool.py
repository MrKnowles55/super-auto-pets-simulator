import random
from src.pet_utils.pet import Pet
from src.team_utils.team import Team
from src.data_utils.pet_data_manager import pet_db
from random import choice


class Pool:
    def __init__(self):
        self.database = pet_db
        self.pool_dict = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
                     }

    # Populate Pool

    def get_pets_by_pack(self, pack):
        for i in range(1, 7):
            self.pool_dict[i] = list(self.database.get_filtered_pet_list(tier=i, pack=pack))

    # Generation Methods

    def generate_pet(self, tier_min=1, tier_max=6):
        if self.pool_dict is None:
            return
        tier = random.randint(tier_min, tier_max)
        pet = random.choice(self.pool_dict[tier])
        return Pet(pet)

    def generate_team(self, action_handler, team_name="Enemy", team_size=5, tier_min=1, tier_max=6):
        team = Team(team_name)
        for i in range(team_size):
            team.add_pet(self.generate_pet(tier_min, tier_max))
        team.action_handler = action_handler
        return team


class TurtlePool(Pool):
    def __init__(self):
        super().__init__()
        self.get_pets_by_pack("Turtle")


if __name__ == "__main__":
    pool = TurtlePool()
    print(pool.generate_team(None, tier_max=1).pets_list)

