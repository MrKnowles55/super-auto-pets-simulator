from abc import abstractmethod
from .ability import Ability
from random import sample
import logger
from pet_data_utils.enums.trigger_event import TriggerEvent
from pet_data_utils.enums.effect_kind import EffectKind
from pet_data_utils.enums.effect_target_kind import EffectTargetKind
from team.team import player_team, opponent_team

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


class DamageRandomEnemy(Damage):
    def apply(self, pet, team, **kwargs):
        # Set enemy team to opposite team
        enemy_team = player_team if self.owner.team == opponent_team else opponent_team
        if enemy_team.pets:
            alive_pets = [p for p in enemy_team.pets if p.is_alive]

            if alive_pets:
                target_pets = sample(alive_pets, min(self.target_n, len(alive_pets)))
            else:
                target_pets = []

            for target_pet in target_pets:
                log.debug(f"{self.owner} dealing {self.damage_amount} damage to {target_pet}")
                target_pet.take_damage(damage=self.damage_amount, attacker=self.owner)
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