class Team:
    def __init__(self):
        self.pets = []

    def add_pet(self, pet, index=None):
        if len(self.pets) < 5:
            if index is not None:
                self.pets.insert(index, pet)
            else:
                self.pets.append(pet)
            pet.team = self

    def remove_pet(self, pet):
        if pet in self.pets:
            self.pets.remove(pet)

    def move_pet(self, old_index, new_index):
        if 0 <= old_index < len(self.pets) and 0 <= new_index < len(self.pets):
            pet = self.pets.pop(old_index)
            self.pets.insert(new_index, pet)
