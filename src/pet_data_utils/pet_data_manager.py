import json
import os
from src.pet_data_utils.enums.trigger_event import TriggerEvent
from src.pet_data_utils.enums.effect_kind import EffectKind
import src.config_utils.logger as logger

log = logger.setup_logger(__name__)

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


class PetDatabase:
    def __init__(self, file_path):
        self.pet_dict = self.load_pet_dict(file_path)
        self.pool_dict = {}

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

    def add_pool(self, pool_name, pool_list):
        if pool_name in self.pool_dict.keys():
            print(f"{pool_name} already exists")
        else:
            self.pool_dict[pool_name] = pool_list
            log.debug(f"Pool Added, {pool_name} : {pool_list}")

    def get_pools_list(self):
        return json.dumps(list(self.pool_dict.keys()))


pet_db = PetDatabase(filename)

IMPLEMENTED = ["Ant", 'Mosquito', "Sloth", "Cricket", "Betta Fish", "Flamingo", 'Anteater', 'Rat',  'Osprey', 'Sheep',
               'Slug', 'Wolf', 'Deer']

TEST_POOL = ['Dolphin', "Cricket", "Mosquito"]  # Rooster
TEST_POOL2 = ['Cricket', 'Dolphin', "Mosquito"]

# Leopard: % of attack
# Crocodile: Last pet
# Dolphin: Least Health Pet


pet_db.add_pool("TEST_POOL", TEST_POOL)
pet_db.add_pool("TEST_POOL2", TEST_POOL2)
pet_db.add_pool("IMPLEMENTED", IMPLEMENTED)
# Priority pets to implement for simpler abilities

PRIORITY = [
    #  SummonPet
    'Fly',
    'Rooster',
    # Tokens
    'Bus',
    'Zombie Fly',
    'Chick',
    #  ModifyStats
    'Boar',
    'Camel',
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

# ANT_LIKE = sorted(pet_data_manager.get_filtered_pet_list(trigger=TriggerEvent.Faint.name,
#                                                          triggered_by_kind="Self",
#                                                          effect_kind=EffectKind.ModifyStats.name))
CRICKET_LIKE = sorted(pet_db.get_filtered_pet_list(trigger=TriggerEvent.Faint.name,
                                                   triggered_by_kind="Self",
                                                   effect_kind=EffectKind.SummonPet.name))
MOSQUITO_LIKE = sorted(pet_db.get_filtered_pet_list(trigger=TriggerEvent.StartOfBattle.name,
                                                   effect_kind=EffectKind.DealDamage.name))


# Tiers
TOKENS = pet_db.get_pets_by_tier("Summoned")
for i in range(1, 7):
    pet_db.add_pool(f"TIER_{i}", pet_db.get_pets_by_tier(i))
pet_db.add_pool("TOKENS", TOKENS)

# Packs
PACK_NAMES = ["Turtle", "Puppy", "Star", "Tiger", "Golden"]
for i in PACK_NAMES:
    pet_db.add_pool(f"{i.upper()}_PACK", pet_db.get_pets_by_pack(i))

# Trigger
pet_db.add_pool("FAINT_PETS", sorted(pet_db.get_pets_by_trigger(TriggerEvent.Faint.name, triggered_by_kind="Self")))

# Ability
MODIFY_STATS_PETS = sorted(pet_db.get_pets_by_effect_kind("ModifyStats"))

# Other
pet_db.add_pool("BUYABLE", list(set({pet["name"] for pet in pet_db.pet_dict.values()}) - set(TOKENS)))

# Add pools to dict

if __name__ == "__main__":
    print(MODIFY_STATS_PETS)
    # print('Ant-Like Pets (Trigger: Faint, Effect: ModifyStats) :', ", ".join(map(str, ANT_LIKE)))
    # print('Cricket-Like Pets (Trigger: Faint, Effect: SummonPet) :', ", ".join(map(str, CRICKET_LIKE)))

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
