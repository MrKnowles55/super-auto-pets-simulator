import json
import os

directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, "../../data/pet_data.json")


def load_pet_dict(file_path):
    with open(file_path) as f:
        return json.load(f)


def get_pets_by_trigger(pet_dict, trigger, triggered_by_kind=None):
    pets = set()

    for pet_name, pet_data in pet_dict.items():
        for level in range(1, 4):
            ability_key = f"level{level}Ability"
            ability_data = pet_data.get(ability_key)

            if not ability_data:
                continue

            if ability_data.get("trigger") == trigger and ability_data.get("triggeredBy", {}).get(
                    "kind") == triggered_by_kind:
                pets.add(pet_name)

    return sorted(pets)


def get_pets_by_tier(pet_dict, tier):
    return [pet for pet, data in pet_dict.items() if data.get("tier") == tier]


PET_DICT = load_pet_dict(filename)
TOKENS = ["Bee", "Bus", "Butterfly", "Chick", "Dirty Rat", "Ram", "Zombie Fly", "Zombie Cricket", "Loyal Chinchilla"]
BUYABLE = list(set(PET_DICT.keys()) - set(TOKENS))

TEST_POOL = ["Ant"]
TEST_POOL2 = ["Cricket", "Hedgehog"]
IMPLEMENTED = []

# Tiers
TIER_1 = get_pets_by_tier(PET_DICT, 1)
TIER_2 = get_pets_by_tier(PET_DICT, 2)
TIER_3 = get_pets_by_tier(PET_DICT, 3)
TIER_4 = get_pets_by_tier(PET_DICT, 4)
TIER_5 = get_pets_by_tier(PET_DICT, 5)
TIER_6 = get_pets_by_tier(PET_DICT, 6)

# abilities
FAINT_PETS = get_pets_by_trigger(PET_DICT, "Faint", triggered_by_kind="Self")

if __name__ == "__main__":
    print("Faint pets:", FAINT_PETS)
    print("Tier 1:", TIER_1)
    print("Tier 2:", TIER_2)
    print("Tier 3:", TIER_3)
    print("Tier 4:", TIER_4)
    print("Tier 5:", TIER_5)
    print("Tier 6:", TIER_6)
