import json
from pet_json_reader import display, load_data, get_incomplete_pets

WIP = "pet_data_wip.json"


def get_pet(data, pet):
    if "pet_utils" not in pet:
        pet = "pet_utils-"+pet
    if pet in data:
        return data[pet]
    else:
        return None


def fix_tier(data, pet):
    pet_dict = get_pet(data, pet)
    if not pet_dict:
        return None
    new_tier = 0
    while new_tier not in [1, 2, 3, 4, 5, 6]:
        new_tier = int(input(f"What Tier is {pet_dict['name']} in: "))
    data[pet_dict["id"]]["tier"] = new_tier
    return data


def fix_pack(data, pet, packs=None):
    pet_dict = get_pet(data, pet)
    if not pet_dict:
        return None
    pack_string = "default"
    new_packs = set()
    pack_dict = {
        "1": "Turtle",
        "2": "Golden",
        "3": "Star",
        "4": "Tiger",
        "5": "Puppy"
    }
    if not packs:
        while pack_string:
            pack_string = input(f"What Pack is {pet_dict['name']} in (1: Turtle, 2: Golden, 3: Star, 4: Tiger, 5: Puppy): ")
            for pack in pack_string:
                if pack in "12345":
                    new_packs.add(pack_dict[pack])
        data[pet_dict["id"]]["packs"] = list(new_packs)
    else:
        data[pet_dict["id"]]["packs"] = packs
    return data


def normalize_packs(data):
    pack_translator = {
        "StandardPack":"Turtle",
        "ExpansionPack1": "Puppy",
        "Weekly": "Tiger",
        "Custom": "",
        "Turtle": "Turtle",
        "Golden": "Golden",
        "Star": "Star",
        "Puppy": "Puppy",
        "Tiger": "Tiger"
    }

    updated_data = data
    for pet_name, pet_data in data.items():
        fixed_packs = []
        for pack in pet_data["packs"]:
            if pack in pack_translator:
                fixed_packs.append(pack_translator[pack])
            else:
                print(pack, "not in translator")
        updated_data = fix_pack(updated_data, pet_name, packs=fixed_packs)

    return updated_data


def fix_stats(data, pet):
    pet_dict = get_pet(data, pet)
    if not pet_dict:
        return None
    attack, health = 0, 0
    while not attack:
        new_attack = input(f"What is the Attack of {pet_dict['name']}: ")
        try:
            new_attack = int(new_attack)
        except ValueError:
            new_attack = 0
            print("Not a valid value")
        if new_attack > 0:
            attack = new_attack
    while not health:
        new_health = input(f"What is the Health of {pet_dict['name']}: ")
        try:
            new_health = int(new_health)
        except ValueError:
            new_health = 0
            print("Not a valid value")
        if new_health > 0:
            health = new_health
    data[pet_dict["id"]]["baseAttack"] = attack
    data[pet_dict["id"]]["baseHealth"] = health
    return data


def fix_ability_description(data, pet):
    pet_dict = get_pet(data, pet)
    if not pet_dict:
        return None
    one = input("Level 1 Ability Description: ")
    two = input("Level 2 Ability Description: ")
    three = input("Level 3 Ability Description: ")
    pet_dict["level1Ability"]["description"] = one
    pet_dict["level2Ability"]["description"] = two
    pet_dict["level3Ability"]["description"] = three
    data[pet] = pet_dict
    return data


def fix_all(data, pet):
    pet_dict = get_pet(data, pet)
    if not pet_dict:
        return None
    pet_dict["tier"] = 0
    pet_dict["baseAttack"] = 0
    pet_dict["baseHealth"] = 0
    pet_dict["packs"] = []
    pet_dict["level1Ability"] = {"description": ""}
    pet_dict["level2Ability"] = {"description": ""}
    pet_dict["level3Ability"] = {"description": ""}
    data[pet] = pet_dict
    data = fix_tier(data, pet)
    data = fix_pack(data, pet)
    data = fix_stats(data, pet)
    data = fix_ability_description(data, pet)
    # new_tier = 0
    # while new_tier not in [1, 2, 3, 4, 5, 6]:
    #     new_tier = int(input(f"What Tier is {pet_dict['name']} in: "))
    # data[pet_dict["id"]]["tier"] = new_tier
    return data


def fix_missing_keywords(data, pet):
    pet_dict = get_pet(data, pet)
    if not pet_dict:
        return None
    print("\n\n\n"+pet_dict["name"])
    print("1:", pet_dict["level1Ability"]["description"])
    print("2:", pet_dict["level2Ability"]["description"])
    print("3:", pet_dict["level3Ability"]["description"])
    trigger = input(f"Trigger: ")
    triggerby = input(f"Triggered By: ")
    effect_kind = input(f"Effect Kind: ")
    pet_dict["level1Ability"]["trigger"] = trigger
    pet_dict["level1Ability"]["triggeredBy"] = {"kind": triggerby}
    pet_dict["level1Ability"]["effect"] = {"kind": effect_kind}

    pet_dict["level2Ability"]["trigger"] = trigger
    pet_dict["level2Ability"]["triggeredBy"] = {"kind": triggerby}
    pet_dict["level2Ability"]["effect"] = {"kind": effect_kind}

    pet_dict["level3Ability"]["trigger"] = trigger
    pet_dict["level3Ability"]["triggeredBy"] = {"kind": triggerby}
    pet_dict["level3Ability"]["effect"] = {"kind": effect_kind}
    data[pet] = pet_dict
    return data


def save_to_wip(data):
    with open("../../data/old/pet_data_wip.json", "w") as file:
        json.dump(data, file, indent=4)


def save_to_main(data):
    with open("../../data/pet_data.json", "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    pet_data = load_data("../../data/pet_data.json")
    # normalize_packs(pet_data)
    # save_to_main(pet_data)
    # pet_to_fix = input("What pet_utils to fix its tier? ").lower()
    # pets_with_bad_tier = get_incomplete_pets(pet_data)["bad_tier"]
    # pets_with_bad_packs = get_incomplete_pets(pet_data)["missing_pack"]
    # pets_with_bad_stats = get_incomplete_pets(pet_data)["bad_stats"]
    # pets_missing_all = get_incomplete_pets(pet_data)["missing_all"]
    # pets_missing_keywords = get_incomplete_pets(pet_data)["missing_ability_keywords"]

    # for pet_utils in pets_missing_keywords:
    #     pet_to_fix = pet_utils
    #     if "pet_utils" not in pet_to_fix:
    #         pet_to_fix = "pet_utils-"+pet_to_fix
    #     pet_data = fix_missing_keywords(pet_data, pet_to_fix)
    #     if not pet_data:
    #         print(f"{pet_utils} Invalid")
    #         continue
    #     display(pet_data[pet_to_fix])
    #     if input("Save to WIP? ").lower() in ["y", "yes", "1"]:
    #         save_to_wip(pet_data)
    #         print(f'Saving {pet_to_fix} to WIP')
    #     else:
    #         print(f'Did NOT save {pet_to_fix} changes.')
