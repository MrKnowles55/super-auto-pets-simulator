import src.logger as logger

log = logger.setup_logger(__name__)


class Team:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def __str__(self):
        return self.name + " Team"

    def add_pet(self, pet, index=None):
        log.debug(f"{self} adding {pet} at index {index}")
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

    def remove_pet(self, pet):
        if pet in self.pets:
            log.debug(f"{self} removing {pet}")
            self.pets.remove(pet)
        else:
            log.debug(f"{self} cannot remove {pet} because it does not exist")

    def move_pet(self, old_index, new_index):
        if 0 <= old_index < len(self.pets) and 0 <= new_index < len(self.pets):
            log.debug(f"{self} moving {self.pets[old_index]} from {old_index} to {new_index}")
            pet = self.pets.pop(old_index)
            self.pets.insert(new_index, pet)
        else:
            try:
                pet = self.pets[old_index]
                log.debug(f"{self} cannot move {pet} from {old_index} to {new_index}")
            except IndexError:
                log.debug(f"{self} has no pet at {old_index} to move.")


player_team = Team("Player")
opponent_team = Team("Opponent")

