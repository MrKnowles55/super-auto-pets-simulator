import json
import os
from src.pet_data_utils.enums.trigger_event import TriggerEvent
from src.pet_data_utils.enums.effect_kind import EffectKind
from src.pet_data_utils.enums.effect_target_kind import EffectTargetKind

directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, "../../data/pet_data.json")


def compare_lists(lst1, lst2):
    set1 = set(lst1)
    set2 = set(lst2)

    if set1.issubset(set2) and set2.issubset(set1):
        print("The sets are the same.")

    diff1 = set1.difference(set2)
    diff2 = set2.difference(set1)

    if len(diff1) > 0 or len(diff2) > 0:
        print("The sets differ in the following elements:")
        print("Set 1:", diff1)
        print("Set 2:", diff2)


class PetData:
    def __init__(self, file_path):
        self.pet_dict = self.load_pet_dict(file_path)

    @staticmethod
    def load_pet_dict(file_path):
        with open(file_path) as f:
            return json.load(f)

    def get_pets_by_trigger(self, trigger, triggered_by_kind=None):
        pets = set()

        for pet_id, pet_data in self.pet_dict.items():
            for level in range(1, 4):
                ability_key = f"level{level}Ability"
                ability_data = pet_data.get(ability_key)

                if not ability_data:
                    continue
                if ability_data.get("trigger") == trigger:
                    if ability_data.get("triggeredBy", {}).get("kind") == triggered_by_kind or not triggered_by_kind:
                        pets.add(pet_data["name"])

        return list(pets)

    def get_pets_by_effect_kind(self, effect_kind):
        pets = set()

        for pet_id, pet_data in self.pet_dict.items():
            for level in range(1, 4):
                ability_key = f"level{level}Ability"
                ability_data = pet_data.get(ability_key)

                if not ability_data:
                    continue

                if ability_data.get("effect").get("kind") == effect_kind:
                    pets.add(pet_data["name"])

        return list(pets)

    def get_pets_by_pack(self, pack):
        pets = []

        for pet_id, pet_data in self.pet_dict.items():
            pack_data = pet_data.get("packs")

            if not pack_data:
                continue

            if pack in pack_data:
                pets.append(pet_data["name"])
        return pets

    def get_pets_by_tier(self, tier):
        pets = []

        for pet_id, pet_data in self.pet_dict.items():
            tier_data = pet_data.get("tier")

            if not tier_data:
                continue

            if tier == tier_data:
                pets.append(pet_data["name"])
        return pets

    def keys(self):
        return self.pet_dict.keys()

    def get_filtered_pet_list(self, trigger=None, triggered_by_kind=None, effect_kind=None, tier=None, pack=None):
        trigger_list = []
        effect_kind_list = []
        tier_list = []
        pack_list = []
        if trigger:
            trigger_list = self.get_pets_by_trigger(trigger=trigger, triggered_by_kind=triggered_by_kind)
            # print(f"Trigger {trigger}:", trigger_list)
        if effect_kind:
            effect_kind_list = self.get_pets_by_effect_kind(effect_kind=effect_kind)
            # print(f"Effect {effect_kind}:", effect_kind_list)
        if tier:
            tier_list = self.get_pets_by_tier(tier=tier)
            # print(f"Tier {tier}:", tier_list)
        if pack:
            pack_list = self.get_pets_by_pack(pack=pack)
            # print(f"Pack {pack}:", pack_list)

        lists = [lst for lst in [trigger_list, effect_kind_list, tier_list, pack_list] if lst]
        # print("Lists", lists)

        intersection = set(lists[0]).intersection(*lists[1:])
        return intersection


pet_data_manager = PetData(filename)

TEST_POOL = ["Ant"]
TEST_POOL2 = ["Cricket"]
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

ANT_LIKE = sorted(pet_data_manager.get_filtered_pet_list(trigger=TriggerEvent.Faint.name,
                                                         triggered_by_kind="Self",
                                                         effect_kind=EffectKind.ModifyStats.name))
CRICKET_LIKE = sorted(pet_data_manager.get_filtered_pet_list(trigger=TriggerEvent.Faint.name,
                                                             triggered_by_kind="Self",
                                                             effect_kind=EffectKind.SummonPet.name))

# Tiers
TIER_1 = pet_data_manager.get_pets_by_tier(1)
TIER_2 = pet_data_manager.get_pets_by_tier(2)
TIER_3 = pet_data_manager.get_pets_by_tier(3)
TIER_4 = pet_data_manager.get_pets_by_tier(4)
TIER_5 = pet_data_manager.get_pets_by_tier(5)
TIER_6 = pet_data_manager.get_pets_by_tier(6)
TOKENS = pet_data_manager.get_pets_by_tier("Summoned")

# Packs
TURTLE_PACK = pet_data_manager.get_pets_by_pack("Turtle")
PUPPY_PACK = pet_data_manager.get_pets_by_pack("Puppy")
STAR_PACK = pet_data_manager.get_pets_by_pack("Star")
TIGER_PACK = pet_data_manager.get_pets_by_pack("Tiger")
GOLDEN_PACK = pet_data_manager.get_pets_by_pack("Golden")

# Trigger
FAINT_PETS = sorted(pet_data_manager.get_pets_by_trigger("Faint", triggered_by_kind="Self"))

# Ability
MODIFY_STATS_PETS = sorted(pet_data_manager.get_pets_by_effect_kind("ModifyStats"))

# Other

BUYABLE = list(set(pet_data_manager.keys()) - set(TOKENS))

if __name__ == "__main__":
    print('Ant-Like Pets (Trigger: Faint, Effect: ModifyStats) :', ", ".join(map(str, ANT_LIKE)))
    print('Cricket-Like Pets (Trigger: Faint, Effect: SummonPet) :', ", ".join(map(str, CRICKET_LIKE)))


    # kinds = {}
    # for pet in PRIORITY:
    #     pet_id = "pet-"+pet.lower().replace(" ", "-")
    #     ability = pet_data_manager.pet_dict[pet_id].get("level1Ability")
    #     if ability:
    #         kind = ability.get("effect").get("kind")
    #         if kind in kinds.keys():
    #             kinds[kind].append(pet)
    #         else:
    #             kinds[kind] = [pet]
    #
    # for k, v in kinds.items():
    #     print("# ", k)
    #     for _ in sorted(v):
    #         print(f"'{_}',")
