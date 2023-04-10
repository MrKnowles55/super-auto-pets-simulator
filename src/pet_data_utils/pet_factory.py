from src.pet import Pet
from src.abilities.ability_generator import AbilityGenerator
from src.pet_data_utils.pet_dict import PET_DICT


def create_pet(pet_name, pet_level=1):
    if 'pet' not in pet_name:
        pet_name = "pet-"+pet_name
    pet_data = PET_DICT[pet_name.lower()]
    name = pet_name.capitalize()
    return Pet(pet_name, pet_data.get("baseAttack"), pet_data.get("baseHealth"), pet_data.get("tier"), pet_level,
               pet_data.get("level1Ability"), pet_data.get("level2Ability"), pet_data.get("level3Ability"),
               AbilityGenerator)