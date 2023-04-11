import json
import os
directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, "../../data/pet_data.json")


def get_faint_pets(pet_dict):
    faint_pets = set()
    for pet_name, pet_data in pet_dict.items():
        for level in range(1, 4):
            ability_key = f"level{level}Ability"
            if ability_key in pet_data:
                ability_data = pet_data[ability_key]
                if "trigger" in ability_data and ability_data["trigger"] == "Faint":
                    if "triggeredBy" in ability_data and ability_data["triggeredBy"].get("kind") == "Self":
                        faint_pets.add(pet_name)
    return sorted(list(faint_pets))


with open(filename) as f:
    PET_DICT = json.load(f)

TEST_POOL = [
    "Ant"
]

TEST_POOL2 = [
    "Cricket",
    "Hedgehog"
]

IMPLEMENTED = [

]

TOKENS = [
    "Zombie Cricket",
    "Loyal Chinchilla"
]

BUYABLE = list(set(list(PET_DICT.keys())) - set(TOKENS))

# Tiers
TIER_1 = [key for key, value in PET_DICT.items() if value.get("tier") == 1]
TIER_2 = [key for key, value in PET_DICT.items() if value.get("tier") == 2]
TIER_3 = [key for key, value in PET_DICT.items() if value.get("tier") == 3]
TIER_4 = [key for key, value in PET_DICT.items() if value.get("tier") == 4]
TIER_5 = [key for key, value in PET_DICT.items() if value.get("tier") == 5]
TIER_6 = [key for key, value in PET_DICT.items() if value.get("tier") == 6]

# Packs


# abilities
FAINT_PETS = get_faint_pets(PET_DICT)

if __name__ == "__main__":
    print("Faint pets:", FAINT_PETS)
    print("Tier 1:", TIER_1)
    print("Tier 2:", TIER_2)
    print("Tier 3:", TIER_3)
    print("Tier 4:", TIER_4)
    print("Tier 5:", TIER_5)
    print("Tier 6:", TIER_6)


