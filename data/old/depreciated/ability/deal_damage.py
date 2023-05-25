from abc import abstractmethod
from .ability_abstract import AbilityBase
from random import choice
from data.old.depreciated.action_utils import *
from src.data_utils.enums.effect_target_kind import EffectTargetKind
from src.config_utils.logger import setup_logger, log_call, log_class_init

log = setup_logger(__name__)


class Damage(AbilityBase):
    def __init__(self, owner, trigger_event, target_type, target_n, damage_amount):
        super().__init__(owner, trigger_event)
        self.damage_amount = damage_amount
        self.target_type = target_type
        self.target_n = target_n
        self.trigger_event = trigger_event

    @log_call(log)
    @abstractmethod
    def apply(self, **kwargs):
        pass

    @staticmethod
    @log_call(log)
    def update_applied_damage(pet, damage, applied_damage):
        if pet not in applied_damage:
            applied_damage[pet] = 0
        applied_damage[pet] += damage
        return applied_damage

    @log_call(log)
    def get_optimal_targets(self, living_pets, applied_damage, mode):
        # target_healths = {pet_utils: pet_utils.health - applied_damage.get(pet_utils, 0) for pet_utils in living_pets}
        target_healths = {pet: pet.health for pet in living_pets}
        log.print(f"target_healths {target_healths}")

        # Filter out pets with health at or below 0
        viable_pets = [pet for pet, health in target_healths.items() if health > 0]
        log.print(f"viable_pets {viable_pets}")

        if not viable_pets:
            return None

        # Get the pet_utils based on the mode
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
        log.print(f"Optimal pet selected: {optimal_pet}")
        return optimal_pet

    @log_call(log)
    def apply_damage(self, enemy_team=None, applied_damage=None):
        actions = []
        if not enemy_team:
            log.print(f"No enemy_team")
            return actions

        # Get the living pets in the enemy team_utils
        living_pets = [pet for pet in enemy_team.pets_list if pet.is_alive]

        if not living_pets:
            log.print(f"No living_pets")
            return actions

        # Get the optimal target
        target_pet = self.get_optimal_targets(living_pets, applied_damage, self.target_type)

        if target_pet:
            # Add the "take_damage" action_utils to the actions list
            actions.append(generate_damage_action(source=self.owner, trigger_event=self.trigger_event, target_pet=target_pet, damage_amount=self.damage_amount))

            # Update the applied damage dictionary
            # self.update_applied_damage(target_pet, self.damage_amount, applied_damage)

        return actions


@log_class_init(log)
class DamageRandomEnemy(Damage):
    @log_call(log)
    def apply(self, enemy_team=None, applied_damage=None, **kwargs):
        return self.apply_damage(enemy_team, applied_damage)


@log_class_init(log)
class DamageEnemyWithAttribute(Damage):
    @log_call(log)
    def apply(self, enemy_team=None, applied_damage=None, **kwargs):
        return self.apply_damage(enemy_team, applied_damage)

    #     elif self.target == "all":
    #         targets = []
    #         # Damage the pets
    #         if team_utils:
    #             for pet_utils in team_utils.pets:
    #                 if pet_utils.is_alive():
    #                     pet_utils.health -= self.damage
    #                     targets.append(pet_utils)
    #         if enemy_team:
    #             for pet_utils in enemy_team.pets:
    #                 if pet_utils.is_alive():
    #                     pet_utils.health -= self.damage
    #                     targets.append(pet_utils)
    #         priority_dict = prioritize_pets(targets)
    #         for target in sorted(priority_dict.keys(), reverse=True):
    #             pets_with_same_priority = priority_dict[target]
    #             for pet_utils in pets_with_same_priority:
    #                 pet_utils.hurt()
    #     elif self.target == "friend_behind":
    #         index = team_utils.pets.index(pet_utils)
    #         if index < 5 and len(team_utils.pets) > 1:
    #             target = team_utils.pets[index + 1]
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