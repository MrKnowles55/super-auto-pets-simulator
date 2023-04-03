from pet import Pet


def create_pet(pet_name, pet_level="1"):
    from pet_dict import PET_DEFAULTS
    pet_data = PET_DEFAULTS[pet_name]
    ability = pet_data["abilities"][pet_level]
    return Pet(pet_name, pet_data["attack"], pet_data["health"], ability)