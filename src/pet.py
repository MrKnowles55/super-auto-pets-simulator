from pet_data_utils.enums.trigger_event import TriggerEvent
from pet_data_utils.enums.effect_kind import EffectKind
from pet_data_utils.enums.effect_target_kind import EffectTargetKind
import logger

log = logger.setup_logger(__name__)


class Pet:
    """
    A class representing a pet in the game.
    """
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
        self.abilities = self.generate_abilities(ability_generator)
        self.ability = self.abilities[self.level]
        self.team = None
        self.fainted = False

    def __str__(self):
        return f"{self.name}({self.attack}/{self.health})"

    def __repr__(self):
        return f"{self.name}({self.attack}/{self.health})"

    @property
    def is_alive(self):
        return self.health > 0

    def generate_abilities(self, ability_generator):
        return {
            lvl: ability_generator(ability_dict, self).generate()
            for lvl, ability_dict in self.ability_dicts.items()
        }

    def attack_pet(self, enemy_pet):
        """
        Attack an enemy pet.

        :param enemy_pet: The enemy pet to attack.
        """
        log.debug(f"{self.name} attacking {enemy_pet.name}")
        self.take_damage(enemy_pet.attack, enemy_pet)
        enemy_pet.take_damage(self.attack, self)

    def take_damage(self, damage, attacker):
        """
        Apply damage to the pet.

        :param damage: The amount of damage to apply.
        :param attacker: The pet dealing the damage.
        """
        log.debug(f"{self.name} took {damage} damage from {attacker}.")
        old_health = self.health
        self.health -= damage

        if self.is_alive:
            if self.health < old_health:
                self.hurt()
        else:
            self.faint(attacker)

    def faint(self, attacker):
        """
        Make the pet faint and trigger its ability if applicable.

        :param attacker: The pet that caused the fainting.
        """
        if not self.fainted:
            self.fainted = True
            log.debug(f"{self.name} fainted")
            if self.ability:
                self.ability.trigger(TriggerEvent.Faint, self, self.team, enemy_team=attacker.team)

            # Clean up dead pets after abilities have been triggered
            if not self.is_alive and self in self.team.pets:
                self.team.remove_pet(self)

    def apply_ability(self, team, enemy_team):
        self.ability.apply(self, team, enemy_team)

    def start_of_battle(self, enemy_team):
        if self.ability:
            self.ability.trigger(TriggerEvent.StartOfBattle, self, self.team, enemy_team=enemy_team)

    def hurt(self):
        if self.ability:
            self.ability.trigger(TriggerEvent.Hurt, self, self.team)

    def before_attack(self):
        if self.ability:
            self.ability.trigger(TriggerEvent.BeforeAttack, self, self.team)


def prioritize_pets(pet_list, priority_key=lambda x: x.attack):
    """
    Create a dictionary of pets prioritized by a given attribute.

    :param pet_list: A list of pets to prioritize.
    :param priority_key: A function that takes a pet and returns a value to prioritize the pet by.
    :return: A dictionary where keys are priorities and values are lists of pets with that priority.
    """
    sorted_pets = sorted(pet_list, key=priority_key, reverse=True)

    priority_dict = {}
    for pet in sorted_pets:
        priority = priority_key(pet)
        if priority not in priority_dict:
            priority_dict[priority] = []
        priority_dict[priority].append(pet)

    return priority_dict


# def filter_pets_by_ability_trigger(pet_list, trigger):
#     """
#     Filter a list of pets based on a given ability trigger.
#
#     :param pet_list: A list of pets to filter.
#     :param trigger: The trigger to filter pets by.
#     :return: A list of pets with the specified ability trigger.
#     """
#     return [pet for pet in pet_list if pet.ability.trigger_event == trigger]
#
#
# def sort_pets_by_attribute(pet_list, attribute, reverse=True):
#     """
#     Sort a list of pets based on a given attribute.
#
#     :param pet_list: A list of pets to sort.
#     :param attribute: The attribute to sort pets by.
#     :param reverse: Whether to sort the pets in descending order.
#     :return: A sorted list of pets based on the specified attribute.
#     """
#     return sorted(pet_list, key=lambda pet: getattr(pet, attribute), reverse=reverse)





