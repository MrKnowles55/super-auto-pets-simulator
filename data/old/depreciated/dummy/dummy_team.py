class Dummy_Team:
    def __init__(self, name="Dummy"):
        self.name = name
        self.pets_list = []

    def add_pet(self, pet, index=None):
        if len(self.pets_list) < 5:
            if index is not None:
                self.pets_list.insert(index, pet)
            else:
                self.pets_list.append(pet)
            pet.team = self
            self.update_positions()
    def remove_pet(self, pet):
        if pet in self.pets_list:
            self.pets_list.remove(pet)

    def update_positions(self):
        for pet in self.pets_list:
            pet.update_position(self.pets_list.index(pet))

    @property
    def length(self):
        return len(self.pets_list)

    @property
    def first(self):
        if self.length:
            return self.pets_list[0]
        else:
            return None

