class Shop:
    def __init__(self):
        self.pets = []

    def generate_pets(self, num_pets=5):
        # Generate num_pets random pets and add them to the shop.
        pass

    def purchase_pet(self, index):
        if 0 <= index < len(self.pets):
            pet = self.pets.pop(index)
            return pet