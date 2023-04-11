import json
import os

directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, "../../data/pet_data.json")


class PetData:
    def __init__(self, file_path):
        self.pet_dict = self.load_pet_dict(file_path)

    @staticmethod
    def load_pet_dict(file_path):
        with open(file_path) as f:
            return json.load(f)

    def get_pets_by_trigger(self, trigger, triggered_by_kind=None):
        pets_dict = {}

        for pet_name, pet_data in self.pet_dict.items():
            for level in range(1, 4):
                ability_key = f"level{level}Ability"
                ability_data = pet_data.get(ability_key)

                if not ability_data:
                    continue

                if ability_data.get("trigger") == trigger and ability_data.get("triggeredBy", {}).get(
                        "kind") == triggered_by_kind:
                    pets_dict[pet_name] = None

        return pets_dict

    def get_pets_by_pack(self, pack):
        pets = []

        for pet_name, pet_data in self.pet_dict.items():
            pack_data = pet_data.get("packs")

            if not pack_data:
                continue

            if pack in pack_data:
                pets.append(pet_name)
        return pets

    def get_pets_by_tier(self, tier):
        return sorted([pet for pet, data in self.pet_dict.items() if data.get("tier") == tier])

    def filter_pets_by_pack_and_tier(self, pack, tier):
        pets_by_pack = self.get_pets_by_pack(pack)
        return sorted([pet for pet, data in self.pet_dict.items() if data.get("tier") == tier and pet in pets_by_pack])

    def keys(self):
        return self.pet_dict.keys()


pet_data = PetData(filename)
TOKENS = ["Bee", "Bus", "Butterfly", "Chick", "Dirty Rat", "Ram", "Zombie Fly", "Zombie Cricket", "Loyal Chinchilla"]
BUYABLE = list(set(pet_data.keys()) - set(TOKENS))

TEST_POOL = ["Ant"]
TEST_POOL2 = ["Cricket", "Hedgehog"]
IMPLEMENTED = []

# Tiers
TIER_1 = pet_data.get_pets_by_tier(1)
TIER_2 = pet_data.get_pets_by_tier(2)
TIER_3 = pet_data.get_pets_by_tier(3)
TIER_4 = pet_data.get_pets_by_tier(4)
TIER_5 = pet_data.get_pets_by_tier(5)
TIER_6 = pet_data.get_pets_by_tier(6)

# Packs
TURTLE_PACK = pet_data.get_pets_by_pack("Turtle")
PUPPY_PACK = pet_data.get_pets_by_pack("Puppy")
STAR_PACK = pet_data.get_pets_by_pack("Star")
TIGER_PACK = pet_data.get_pets_by_pack("Tiger")
GOLDEN_PACK = pet_data.get_pets_by_pack("Golden")

# abilities
FAINT_PETS = pet_data.get_pets_by_trigger("Faint", triggered_by_kind="Self")

# Other
TIER_1_TURTLE_PACK = pet_data.filter_pets_by_pack_and_tier("Turtle", 1)

if __name__ == "__main__":
    print(TIER_1_TURTLE_PACK)
    print(TIER_1)
    print(TURTLE_PACK)