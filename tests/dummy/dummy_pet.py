from tests.dummy.dummy_ability import generate_dummy_ability


class DummyPet:
    def __init__(self, name="test pet", attack=1, health=1, tier=1, level=1, ability1=None, ability2=None, ability3=None, ability_generator=None):
        self.name = name
        self.attack = attack
        self.health = health
        self.tier = tier
        self.level = level
        self.position = -1
        self.ability_dicts = {
            1: {},
            2: {},
            3: {}
        }
        self.abilities = {
            1: generate_dummy_ability(None),
            2: generate_dummy_ability(None),
            3: generate_dummy_ability(None)
        }
        self.ability = self.abilities[self.level]
        self.team = None
        self.fainted = False

    def display(self, **kwargs):
        output = []
        if not kwargs:
            return f"{self.name}, ({self.attack}/{self.health})"
        for key, value in kwargs.items():
            if hasattr(self, key):
                output.append(f"{getattr(self, key)}")
        return ', '.join(output)

    def before_attack(self):
        return

    def attack_pet(self, other_pet):
        return

    def after_attack(self):
        return

    def start_of_battle(self, enemy_team):
        return


def generate_dummy_pet(name="test pet", attack=1, health=1, tier=1, level=1, ability1=None, ability2=None, ability3=None, ability_generator=None):
    return DummyPet(name, attack, health, tier, level, ability1, ability2, ability3, ability_generator)
