from src.pet_data_utils.enums.trigger_event import TriggerEvent
import config_utils.logger as logger
from action.action_utils import action_handler

log = logger.setup_logger(__name__)


class PetEntity:
    """
    A class representing a pet in the game.
    """
    def __init__(self, name, attack, health, tier, level, ability1, ability2, ability3, ability_generator):
        self.name = name
        self.attack = attack
        self.health = health
        self.tier = tier
        self.level = level
        self.position = -1
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
        return f"{self.name}({self.attack}/{self.health}/P:{self.position})"

    def __repr__(self):
        return f"{self.name}({self.attack}/{self.health}/P:{self.position})"

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
        log.debug(f"{self} attacking {enemy_pet}")
        self.apply_damage(enemy_pet.attack, enemy_pet)
        enemy_pet.apply_damage(self.attack, self)

    def take_damage(self, damage, attacker):
        """
        Create a list of actions to apply damage to the pet.

        :param damage: The amount of damage to apply.
        :param attacker: The pet dealing the damage.
        :return: A list of actions to apply damage to the pet.
        """
        actions = []
        actions.append(("take_damage", self, damage, attacker))
        return actions

    def apply_damage(self, damage, attacker):
        log.debug(f"{self} took {damage} damage from {attacker}.")
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
            log.debug(f"{self} fainted")
            if self.ability:
                actions = self.ability.trigger(TriggerEvent.Faint, self, self.team, enemy_team=attacker.team)
                action_handler.add(actions)

            # Clean up dead pets after abilities have been triggered,
            # Pets that summon pets on faint may remove themselves from the team during the ability
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








