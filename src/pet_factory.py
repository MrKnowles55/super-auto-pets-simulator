from pet import Pet
from ability.ability_generator import AbilityGenerator
from pet_data_utils.pet_data_manager import pet_db


def create_pet(pet_id, pet_level=1):
    if 'pet' not in pet_id:
        pet_id = "pet-" + pet_id.lower().replace(" ", "_")
    pet_data = pet_db.pet_dict[pet_id]
    pet_name = pet_data.get("name")
    return Pet(pet_name, pet_data.get("baseAttack"), pet_data.get("baseHealth"), pet_data.get("tier"), pet_level,
               pet_data.get("level1Ability"), pet_data.get("level2Ability"), pet_data.get("level3Ability"),
               AbilityGenerator)
