import json
import os

directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, "../../data/pet_data.json")


def display(data):
    print(json.dumps(data, indent=4))


def load_data(file=filename):
    with open(file, "r") as f:
        return json.load(f)


def get_attribute(data, attribute, subattribute=None):
    output = {}
    for id, pet_data in data.items():
        temp = pet_data.get(attribute)
        if not temp:
            for key, value in pet_data.items():
                try:
                    temp = pet_data[key][attribute]
                except Exception as e:
                    pass
                if temp and subattribute:
                    try:
                        temp = pet_data[key][attribute][subattribute]
                    except Exception as e:
                        pass
        output[id] = temp
    return output


def get_incomplete_pets(data):
    incomplete_pets = {}
    missing_all = []
    bad_tier = []
    bad_pack = []
    bad_stats = []
    missing_ability_keywords = []
    for key, value in data.items():
        if "tier" not in value:
            missing_all.append(value["id"])
            continue
        elif value["tier"] == 0:
            bad_tier.append(value["id"])

        if not value["packs"]:
            bad_pack.append(value["id"])

        if not isinstance(value["baseAttack"], int) or not isinstance(value["baseHealth"], int):
            bad_stats.append(value["id"])
        elif value["baseAttack"] < 0 or value["baseHealth"] < 0:
            bad_stats.append(value["id"])

        if "level1Ability" in value:
            if "trigger" not in value["level1Ability"]:
                missing_ability_keywords.append(value["id"])

    incomplete_pets["missing_all"] = missing_all
    incomplete_pets["bad_tier"] = bad_tier
    incomplete_pets["missing_pack"] = bad_pack
    incomplete_pets["bad_stats"] = bad_stats
    incomplete_pets["missing_ability_keywords"] = missing_ability_keywords
    return incomplete_pets


def check_pet_data_status(file="pet_data.json"):
    data = load_data(file)
    incomplete_pets = get_incomplete_pets(data)
    problems = 0
    total_pets = len(list(data.keys()))
    bad_pets = set()
    for problem, pets in incomplete_pets.items():
        problems += len(pets)
        print(f"{problem} ({len(pets)}) : {pets}")
        for pet in pets:
            bad_pets.add(pet)
    print(f"{problems} number of issues with pets to resolve.")
    print(f"{len(bad_pets)} bad pets of {total_pets} Total pets. {1-len(bad_pets)/total_pets:.0%} are pets are Good Bois")
    return incomplete_pets


def get_example_pet(trigger, full=False, just_ability=False):
    data = load_data()

    for pet, value in data.items():
        if value["level1Ability"]:
            if value["level1Ability"]["trigger"] == trigger:
                output = value
                if just_ability:
                    output = {k: v for k, v in value.items() if k in ['level1Ability', 'level2Ability', 'level3Ability']}
                elif not full:
                    output = {k: v for k, v in value.items() if k not in ['image', 'probabilities']}

                return output


def get_ability_intersection(effect=False):
    data = load_data()
    list_of_abilities = []
    for pet, value in data.items():
        if "level1Ability" in list(value.keys()):
            if "trigger" in list(value["level1Ability"].keys()):
                if effect:
                    list_of_abilities.append(value["level1Ability"]["effect"])
                else:
                    list_of_abilities.append(value["level1Ability"])
        if "level2Ability" in list(value.keys()):
            if "trigger" in list(value["level2Ability"].keys()):
                if effect:
                    list_of_abilities.append(value["level2Ability"]["effect"])
                else:
                    list_of_abilities.append(value["level2Ability"])
        if "level3Ability" in list(value.keys()):
            if "trigger" in list(value["level3Ability"].keys()):
                if effect:
                    list_of_abilities.append(value["level3Ability"]["effect"])
                else:
                    list_of_abilities.append(value["level3Ability"])

    common_keys = set.intersection(*[set(d.keys()) for d in list_of_abilities])
    print(common_keys)


if __name__ == "__main__":
    data = load_data()
    x = get_attribute(data, "triggered_by")
    for pet, value in x.items():
        l = len(value) if value else 0
        if l and l != 1:
            print(value)
    # check_pet_data_status(file="../../data/old/pet_data_wip.json")

    # display(get_example_pet("Sell", just_ability=True))
    # get_ability_intersection()
    # get_ability_intersection(effect=True)
