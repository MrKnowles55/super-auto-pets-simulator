from data.old.depreciated.dummy.dummy_ability import generate_dummy_ability


class DummyPet:
    def __init__(self, name="test pet_utils", attack=1, health=1, tier=1, level=1, ability1=None, ability2=None, ability3=None, ability_generator=None):
        self.name = name
        self.attack = attack
        self.health = health
        self.tier = tier
        self.level = level
        self.start_position = -1
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

    @property
    def is_alive(self):
        return self.health > 0

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

    def update_position(self, new_position):
        self.position = new_position
        if self.start_position == -1:
            self.start_position = self.position

    def apply_damage(self, damage, attacker):
        self.health -= damage


def generate_dummy_pet(name="test pet_utils", attack=1, health=1, tier=1, level=1, ability1=None, ability2=None, ability3=None, ability_generator=None):
    return DummyPet(name, attack, health, tier, level, ability1, ability2, ability3, ability_generator)


def generate_small_pet():
    return generate_dummy_pet(name="small pet_utils", attack=1, health=1)


def generate_big_pet():
    return generate_dummy_pet(name="big pet_utils", attack=50, health=50)


def generate_strong_pet():
    return generate_dummy_pet(name="strong pet_utils", attack=50, health=1)


def generate_tank_pet():
    return generate_dummy_pet(name="tank pet_utils", attack=0, health=50)