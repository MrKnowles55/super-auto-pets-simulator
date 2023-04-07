from pet import Pet
from ability_generator import AbilityGenerator


def create_pet(pet_name, pet_level=1):
    from Data.extract_data_dicts import PET_DICT
    pet_data = PET_DICT["pet-"+pet_name.lower()]
    name = pet_name.capitalize()
    return Pet(pet_name, pet_data.get("baseAttack"), pet_data.get("baseHealth"), pet_data.get("tier"), pet_level,
               pet_data.get("level1Ability"), pet_data.get("level2Ability"), pet_data.get("level3Ability"),
               AbilityGenerator)