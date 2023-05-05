from src.pet_data_utils.enums.trigger_event import TriggerEvent
from src.config_utils.logger import setup_logger, log_call, log_class_init
from src.action.action_utils import action_handler

log = setup_logger(__name__)


@log_class_init(log)
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

    @log_call(log)
    def attack_pet(self, enemy_pet):
        """
        Attack an enemy pet.

        :param enemy_pet: The enemy pet to attack.
        """
        self.apply_damage(enemy_pet.attack, enemy_pet)
        enemy_pet.apply_damage(self.attack, self)

    # @log_call(log)
    # def take_damage(self, damage, attacker):
    #     """
    #     Create a list of actions to apply damage to the pet.
    #
    #     :param damage: The amount of damage to apply.
    #     :param attacker: The pet dealing the damage.
    #     :return: A list of actions to apply damage to the pet.
    #     """
    #     actions = []
    #     actions.append(("take_damage", self, damage, attacker))
    #     return actions

    @log_call(log)
    def apply_damage(self, damage, attacker):
        old_health = self.health
        self.health -= damage

        if self.is_alive:
            if self.health < old_health:
                self.hurt()
        else:
            self.faint(attacker)

    @log_call(log)
    def faint(self, attacker):
        """
        Make the pet faint and trigger its ability if applicable.

        :param attacker: The pet that caused the fainting.
        """
        if not self.fainted:
            self.fainted = True
            if self.ability:
                actions = self.ability.trigger(TriggerEvent.Faint, enemy_team=attacker.team)
                action_handler.add_action(actions)

            # Clean up dead pets after abilities have been triggered,
            # Pets that summon pets on faint may remove themselves from the team during the ability
            if not self.is_alive and self in self.team.pets:
                self.team.remove_pet(self)

    @log_call(log)
    def hurt(self):
        if self.ability:
            actions = self.ability.trigger(TriggerEvent.Hurt)
            action_handler.add_action(actions)

    @log_call(log)
    def before_attack(self):
        if self.ability:
            actions = self.ability.trigger(TriggerEvent.BeforeAttack)
            action_handler.add_action(actions)








