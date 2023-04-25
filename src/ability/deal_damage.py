from abc import abstractmethod
from .ability import Ability
from random import sample, choice
import src.logger as logger
from src.utils import *
from src.pet_data_utils.enums.trigger_event import TriggerEvent
from src.pet_data_utils.enums.effect_kind import EffectKind
from src.pet_data_utils.enums.effect_target_kind import EffectTargetKind
from src.team.team import player_team, opponent_team

log = logger.setup_logger(__name__)


class Damage(Ability):
    def __init__(self, owner, trigger_event, target_type, target_n, damage_amount):
        super().__init__(owner, trigger_event)
        self.damage_amount = damage_amount
        self.target_type = target_type
        self.target_n = target_n
        self.trigger_event = trigger_event

    @abstractmethod
    def apply(self, pet, team, **kwargs):
        pass

    @staticmethod
    def update_applied_damage(pet, damage, applied_damage):
        if pet not in applied_damage:
            applied_damage[pet] = 0
        applied_damage[pet] += damage
        return applied_damage

    @staticmethod
    def get_optimal_targets(living_pets, applied_damage, mode):
        target_healths = {pet: pet.health - applied_damage.get(pet, 0) for pet in living_pets}

        # Filter out pets with health at or below 0
        viable_pets = [pet for pet, health in target_healths.items() if health > 0]

        if not viable_pets:
            return None

        # Get the pet based on the mode
        match mode:
            case EffectTargetKind.LowestHealthEnemy:
                min_value = min(target_healths[pet] for pet in viable_pets)
                pets_with_min_value = [pet for pet in viable_pets if target_healths[pet] == min_value]
                optimal_pet = choice(pets_with_min_value)
            case EffectTargetKind.HighestHealthEnemy:
                max_value = max(target_healths[pet] for pet in viable_pets)
                pets_with_max_value = [pet for pet in viable_pets if target_healths[pet] == max_value]
                optimal_pet = choice(pets_with_max_value)
            case EffectTargetKind.RandomEnemy:
                optimal_pet = choice(viable_pets)
            case _:
                raise ValueError(f"Invalid mode: {mode}. an EffectTargetKind.")

        return optimal_pet


class DamageRandomEnemy(Damage):
    def apply(self, owner, team, enemy_team=None, priority=None, applied_damage=None):
        actions = []
        if not enemy_team:
            return actions

        # Get the living pets in the enemy team
        living_pets = [pet for pet in enemy_team.pets if pet.is_alive]

        if not living_pets:
            return actions

        # Get the optimal target
        target_pet = self.get_optimal_targets(living_pets, applied_damage, self.target_type)

        if target_pet:
            # Add the "take_damage" action to the actions list
            actions.append(("take_damage", target_pet, self.damage_amount, owner))
            log.debug(f"{self.owner} dealing {self.damage_amount} to {target_pet}")

            # Update the applied damage dictionary
            self.update_applied_damage(target_pet, self.damage_amount, applied_damage)

        return actions


class DamageEnemyWithAttribute(Damage):
    def apply(self, owner, team, enemy_team=None, priority=None, applied_damage=None):
        actions = []
        if not enemy_team:
            return actions

        # Get the living pets in the enemy team
        living_pets = [pet for pet in enemy_team.pets if pet.is_alive]

        if not living_pets:
            return actions

        # Get the optimal target
        target_pet = self.get_optimal_targets(living_pets, applied_damage, mode=self.target_type)

        if target_pet:
            # Add the "take_damage" action to the actions list
            actions.append(("take_damage", target_pet, self.damage_amount, owner))
            log.debug(f"{self.owner} dealing {self.damage_amount} to {target_pet}")

            # Update the applied damage dictionary
            self.update_applied_damage(target_pet, self.damage_amount, applied_damage)

        return actions
    #     elif self.target == "all":
    #         targets = []
    #         # Damage the pets
    #         if team:
    #             for pet in team.pets:
    #                 if pet.is_alive():
    #                     pet.health -= self.damage
    #                     targets.append(pet)
    #         if enemy_team:
    #             for pet in enemy_team.pets:
    #                 if pet.is_alive():
    #                     pet.health -= self.damage
    #                     targets.append(pet)
    #         priority_dict = prioritize_pets(targets)
    #         for target in sorted(priority_dict.keys(), reverse=True):
    #             pets_with_same_priority = priority_dict[target]
    #             for pet in pets_with_same_priority:
    #                 pet.hurt()
    #     elif self.target == "friend_behind":
    #         index = team.pets.index(pet)
    #         if index < 5 and len(team.pets) > 1:
    #             target = team.pets[index + 1]
    #
    #             if target:
    #                 target.health -= self.damage
    #                 target.hurt()
    #     else:
    #         print(f'{self.__class__}:{self.target} not implemented')
    #
    # def trigger(self, event, *args, **kwargs):
    #     if event == self.trigger_event:
    #         self.apply(*args, **kwargs)