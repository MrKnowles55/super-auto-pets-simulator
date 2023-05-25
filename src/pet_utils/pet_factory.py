from data.old.depreciated.pet_entity import PetEntity
from data.old.depreciated.ability.ability_generator import AbilityGenerator
from src.data_utils.pet_data_manager import pet_db
from src.config_utils.logger import setup_logger, log_call
from data.old.depreciated.action_utils import action_handler

log = setup_logger(__name__)


@log_call(log)
def create_pet(pet_id, pet_level=1):
    if 'pet_utils' not in pet_id:
        pet_id = "pet_utils-" + pet_id.lower().replace(" ", "_")
    pet_data = pet_db.pet_dict[pet_id]
    pet_name = pet_data.get("name")
    return PetEntity(pet_name, pet_data.get("baseAttack"), pet_data.get("baseHealth"), pet_data.get("tier"), pet_level,
                     pet_data.get("level1Ability"), pet_data.get("level2Ability"), pet_data.get("level3Ability"),
                     AbilityGenerator, action_handler)
