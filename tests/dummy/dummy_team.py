class Dummy_Team:
    def __init__(self, name="Dummy"):
        self.name = name
        self.pets_list = []

    def add_pet(self, pet):
        self.pets_list.append(pet)

    def remove_pet(self, pet):
        if pet in self.pets_list:
            self.pets_list.remove(pet)

    @property
    def length(self):
        return len(self.pets_list)

    @property
    def first(self):
        if self.length:
            return self.pets_list[0]
        else:
            return None

