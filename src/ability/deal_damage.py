from abc import abstractmethod
from .ability_abstract import AbilityBase
from random import choice
from src.action.action_utils import *
from src.pet_data_utils.enums.effect_target_kind import EffectTargetKind
from config_utils.logger import setup_logger, log_call, log_class_init

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
        log.debug(f"Updating applied_damage. Before: {applied_damage}")
        if pet not in applied_damage:
            applied_damage[pet] = 0
        applied_damage[pet] += damage
        log.debug(f"Updated applied_damage. After: {applied_damage}")
        return applied_damage

    @log_call(log)
    def get_optimal_targets(self, living_pets, applied_damage, mode):
        log.debug(f"Getting optimal targets for {self.__class__.__name__} of {self.owner} with mode {mode}")
        target_healths = {pet: pet.health - applied_damage.get(pet, 0) for pet in living_pets}
        log.debug(f"target_healths {target_healths}")

        # Filter out pets with health at or below 0
        viable_pets = [pet for pet, health in target_healths.items() if health > 0]
        log.debug(f"viable_pets {viable_pets}")

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
        log.debug(f"Optimal pet selected: {optimal_pet}")
        return optimal_pet

    @log_call(log)
    def apply_damage(self, enemy_team=None, applied_damage=None):
        log.debug(f"{self.__class__.__name__} using generic apply_damage()")
        actions = []
        if not enemy_team:
            log.debug(f"No enemy_team")
            return actions

        # Get the living pets in the enemy team
        living_pets = [pet for pet in enemy_team.pets if pet.is_alive]

        if not living_pets:
            log.debug(f"No living_pets")
            return actions

        # Get the optimal target
        target_pet = self.get_optimal_targets(living_pets, applied_damage, self.target_type)

        if target_pet:
            # Add the "take_damage" action to the actions list
            actions.append(generate_damage_action(self.owner, target_pet=target_pet, damage_amount=self.damage_amount))

            # Update the applied damage dictionary
            self.update_applied_damage(target_pet, self.damage_amount, applied_damage)

        return actions


@log_class_init(log)
class DamageRandomEnemy(Damage):
    @log_call(log)
    def apply(self, enemy_team=None, applied_damage=None):
        log.debug(f"Applying {self.__class__.__name__} from {self.owner} on team {self.owner.team}")
        return self.apply_damage(enemy_team, applied_damage)


@log_class_init(log)
class DamageEnemyWithAttribute(Damage):
    @log_call(log)
    def apply(self, enemy_team=None, applied_damage=None):
        return self.apply_damage(enemy_team, applied_damage)

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