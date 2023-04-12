from src.pet_data_utils.enums.trigger_event import TriggerEvent
from src.pet_data_utils.enums.effect_kind import EffectKind
from src.pet_data_utils.enums.effect_target_kind import EffectTargetKind

class Pet:
    def __init__(self, name, attack, health, tier, level, ability1, ability2, ability3, ability_generator):
        self.name = name
        self.attack = attack
        self.health = health
        self.tier = tier
        self.level = level
        self.ability_dicts = {
            1: ability1,
            2: ability2,
            3: ability3
        }
        self.abilities = {
            lvl: ability_generator(ability_dict, self).generate()
            for lvl, ability_dict in self.ability_dicts.items()
        }
        self.ability = self.abilities[self.level]
        self.team = None
        self.fainted = False

    def __str__(self):
        return f"{self.name}({self.attack}/{self.health})"

    def __repr__(self):
        return f"{self.name}({self.attack}/{self.health})"

    def is_alive(self):
        return self.health > 0

    def attack_pet(self, enemy_pet):
        old_self_health, old_enemy_health = self.health, enemy_pet.health

        self.health -= enemy_pet.attack
        enemy_pet.health -= self.attack

        if self.is_alive():
            if self.health < old_self_health:
                self.ability.trigger(TriggerEvent.Faint, self, self.team)

        if enemy_pet.is_alive():
            if enemy_pet.health < old_enemy_health:
                enemy_pet.ability.trigger(TriggerEvent.Hurt, enemy_pet, enemy_pet.team)

        if not self.is_alive() or not enemy_pet.is_alive():
            if not self.is_alive():
                self.ability.trigger(TriggerEvent.Faint, self, self.team, enemy_team=enemy_pet.team)
            if not enemy_pet.is_alive():
                enemy_pet.ability.trigger(TriggerEvent.Faint, enemy_pet, enemy_pet.team, enemy_team=self.team)

            # Clean up dead pets after ability have been triggered
            if not self.is_alive() and self in self.team.pets:
                self.team.remove_pet(self)
            if not enemy_pet.is_alive() and enemy_pet in enemy_pet.team.pets:
                enemy_pet.team.remove_pet(enemy_pet)

    def faint(self):
        if not self.fainted:
            self.fainted = True
            if self.ability:
                self.ability.trigger(TriggerEvent.Faint, self, self.team)

    def apply_ability(self, team, enemy_team):
        self.ability.apply(self, team, enemy_team)

    def start_of_battle(self, enemy_team):
        if self.ability:
            self.ability.trigger(TriggerEvent.StartOfBattle, self, self.team, enemy_team=enemy_team)

    def hurt(self):
        if self.ability:
            self.ability.trigger(TriggerEvent.Hurt, self, self.team)

        if not self.is_alive() and not self.fainted:
            self.faint()
            self.team.remove_pet(self)

    def before_attack(self):
        if self.ability:
            self.ability.trigger(TriggerEvent.BeforeAttack, self, self.team)


def prioritize_pets(pet_list, priority_key=lambda x: x.attack):
    sorted_pets = sorted(pet_list, key=priority_key, reverse=True)

    priority_dict = {}
    for pet in sorted_pets:
        priority = priority_key(pet)
        if priority not in priority_dict:
            priority_dict[priority] = []
        priority_dict[priority].append(pet)

    return priority_dict


def filter_pets_by_ability_trigger(pet_list, trigger):
    return [pet for pet in pet_list if pet.ability.trigger_event == trigger]


def sort_pets_by_attribute(pet_list, attribute, reverse=True):
    return sorted(pet_list, key=lambda pet: getattr(pet, attribute), reverse=reverse)





