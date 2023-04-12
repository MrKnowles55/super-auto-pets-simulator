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


pet_data_manager = PetData(filename)
TOKENS = ["Bee", "Bus", "Butterfly", "Chick", "Dirty Rat", "Ram", "Zombie Fly", "Zombie Cricket", "Loyal Chinchilla"]
BUYABLE = list(set(pet_data_manager.keys()) - set(TOKENS))

TEST_POOL = ["Ant"]
TEST_POOL2 = ["Cricket", "Hedgehog"]
IMPLEMENTED = ["Ant", "Sloth"]

# Priority pets to implement for simpler abilities

PRIORITY = [
    #  SummonPet
    'Cricket',
    'Deer',
    'Fly',
    'Rat',
    'Rooster',
    'Sheep',
    # Tokens
    'Zombie Cricket',
    'Bus',
    'Zombie Fly',
    'Dirty Rat',
    'Chick',
    'Ram',
    #  ModifyStats
    'Boar',
    'Camel',
    'Flamingo',
    'Hippo',
    'Horse',
    'Kangaroo',
    'Mammoth',
    'Peacock',
    'Turkey',
    #  DealDamage
    'Badger',
    'Blowfish',
    'Crocodile',
    'Dolphin',
    'Elephant',
    'Hedgehog',
    'Leopard',
    'Mosquito',
    'Rhino',
    'Snake',
    #  TransferStats
    'Crab',
    'Dodo',
    #  SummonRandomPet
    'Spider',
    #  OneOf (Picks 1 of 2 abilities)
    'Dog',
    #  ApplyStatus
    'Gorilla',
    'Turtle',
    #  AllOf (2 abilities with the same trigger)
    'Ox',
    #  TransferAbility
    'Parrot',
    #  ReduceHealth
    'Skunk',
    #  Swallow
    'Whale',
    #  RepeatAbility
    'Tiger',
]

# Tiers
TIER_1 = pet_data_manager.get_pets_by_tier(1)
TIER_2 = pet_data_manager.get_pets_by_tier(2)
TIER_3 = pet_data_manager.get_pets_by_tier(3)
TIER_4 = pet_data_manager.get_pets_by_tier(4)
TIER_5 = pet_data_manager.get_pets_by_tier(5)
TIER_6 = pet_data_manager.get_pets_by_tier(6)

# Packs
TURTLE_PACK = pet_data_manager.get_pets_by_pack("Turtle")
PUPPY_PACK = pet_data_manager.get_pets_by_pack("Puppy")
STAR_PACK = pet_data_manager.get_pets_by_pack("Star")
TIGER_PACK = pet_data_manager.get_pets_by_pack("Tiger")
GOLDEN_PACK = pet_data_manager.get_pets_by_pack("Golden")

# ability
FAINT_PETS = pet_data_manager.get_pets_by_trigger("Faint", triggered_by_kind="Self")

# Other
TIER_1_TURTLE_PACK = pet_data_manager.filter_pets_by_pack_and_tier("Turtle", 1)
TIER_2_TURTLE_PACK = pet_data_manager.filter_pets_by_pack_and_tier("Turtle", 2)
TIER_3_TURTLE_PACK = pet_data_manager.filter_pets_by_pack_and_tier("Turtle", 3)
TIER_4_TURTLE_PACK = pet_data_manager.filter_pets_by_pack_and_tier("Turtle", 4)
TIER_5_TURTLE_PACK = pet_data_manager.filter_pets_by_pack_and_tier("Turtle", 5)
TIER_6_TURTLE_PACK = pet_data_manager.filter_pets_by_pack_and_tier("Turtle", 6)

if __name__ == "__main__":
    kinds = {}
    for pet in PRIORITY:
        pet_id = "pet-"+pet.lower().replace(" ", "-")
        ability = pet_data_manager.pet_dict[pet_id].get("level1Ability")
        if ability:
            kind = ability.get("effect").get("kind")
            if kind in kinds.keys():
                kinds[kind].append(pet)
            else:
                kinds[kind] = [pet]

    for k, v in kinds.items():
        print("# ", k)
        for _ in sorted(v):
            print(f"'{_}',")