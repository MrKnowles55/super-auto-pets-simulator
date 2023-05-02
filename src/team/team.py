from src.config_utils.logger import setup_logger, log_call, log_class_init
from src.action.action_utils import action_handler, generate_fill_action

log = setup_logger(__name__)


@log_class_init(log)
class Team:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def __str__(self):
        return self.name + " Team"

    @log_call(log)
    def add_pet(self, pet, index=None):
        if len(self.pets) < 5:
            if index is not None:
                self.pets.insert(index, pet)
                pet.position = index
            else:
                self.pets.append(pet)
                pet.position = len(self.pets) - 1
            pet.team = self
        else:
            log.debug(f"{self} is full and cannot add {pet} at index {index}.")

    @log_call(log)
    def remove_pet(self, pet):
        if pet in self.pets:
            self.pets.remove(pet)
            action_handler.add_action(generate_fill_action(self, None))
        else:
            log.debug(f"{self} cannot remove {pet} because it does not exist")

    @log_call(log)
    def move_pet(self, old_index, new_index):
        if 0 <= old_index < len(self.pets) and 0 <= new_index < len(self.pets):
            pet = self.pets.pop(old_index)
            self.pets.insert(new_index, pet)
        else:
            try:
                pet = self.pets[old_index]
                log.debug(f"{self} cannot move {pet} from {old_index} to {new_index}")
            except IndexError:
                log.debug(f"{self} has no pet at {old_index} to move.")

    @log_call(log)
    def fill(self):
        self.pets = [pet for pet in self.pets if pet is not None]
        for i, pet in enumerate(self.pets):
            pet.position = i


player_team = Team("Player")
opponent_team = Team("Opponent")

