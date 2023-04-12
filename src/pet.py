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
        damage_dealt_to_self = enemy_pet.attack
        damage_dealt_to_enemy = self.attack

        self.take_damage(damage_dealt_to_self, enemy_pet)
        enemy_pet.take_damage(damage_dealt_to_enemy, self)

    def take_damage(self, damage, attacker):
        old_health = self.health
        self.health -= damage

        if self.is_alive():
            if self.health < old_health:
                self.hurt()
        else:
            self.faint(attacker)

    def faint(self, attacker):
        if not self.fainted:
            self.fainted = True
            if self.ability:
                self.ability.trigger(TriggerEvent.Faint, self, self.team, enemy_team=attacker.team)

            # Clean up dead pets after abilities have been triggered
            if not self.is_alive() and self in self.team.pets:
                self.team.remove_pet(self)

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





