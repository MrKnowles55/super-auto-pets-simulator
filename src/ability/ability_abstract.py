from abc import ABC, abstractmethod
from random import choice
from src.pet_data_utils.enums.effect_kind import EffectKind
from src.pet_data_utils.enums.effect_target_kind import EffectTargetKind
from src.pet_data_utils.enums.trigger_event import TriggerEvent
import src.logger as logger

log = logger.setup_logger(__name__)


class AbilityBase(ABC):

    def __init__(self, owner, trigger_event=None):
        self.owner = owner
        self.trigger_event = trigger_event
        log.debug(f"{self.__class__.__name__} created for {self.owner} with trigger {self.trigger_event}")

    @abstractmethod
    def apply(self, pet, team, **kwargs):
        pass

    def trigger(self, event, *args, **kwargs):
        if event == self.trigger_event:
            self.apply(*args, **kwargs)

    def __repr__(self):
        attributes = ', '.join([f"{k}={repr(v)}" for k, v in vars(self).items()])
        return f"{self.__class__.__name__}({attributes})"


class No_Ability(AbilityBase):
    def __init__(self, owner):
        super().__init__(owner)

    def apply(self, pet, team, **kwargs):
        pass


# class Summon(Ability):
#     def __init__(self, owner, token, trigger_event, team_to_summon_to):
#         super().__init__(owner)
#         self.token = token
#         self.trigger_event = trigger_event
#         self.team = team_to_summon_to
#
#     def apply(self, pet, team, **kwargs):
#         from pet_factory import create_pet
#         if self.trigger_event == TriggerEvent.Faint:
#
#             index = team.pets.index(pet)
#
#             try:
#                 new_pet = create_pet(self.token)
#                 team.remove_pet(pet)
#                 team.add_pet(new_pet, index)
#             except KeyError:
#                 print(f"Cannot create pet of type {self.token}")
#                 team.remove_pet(pet)
#
#         else:
#             print(f'{self.__class__}:{self.trigger_event} not implemented')
#
#     def trigger(self, event, *args, **kwargs):
#         if event == self.trigger_event:
#             self.apply(*args, **kwargs)


# class Damage(Ability):
#     def __init__(self, damage, target, trigger_event):
#         self.damage = damage
#         self.target = target
#         self.trigger_event = trigger_event
#
#     def apply(self, pet, team, **kwargs):
#         enemy_team = kwargs.get('enemy_team', None)
#         if enemy_team is None:
#             pass
#             # print(f'Error: enemy_team is not provided for {self}')
#             # raise ValueError
#         if self.target == "random_enemy":
#             if enemy_team.pets:
#                 alive_pets = [p for p in enemy_team.pets if p.is_alive()]
#
#                 if alive_pets:
#                     target_pet = choice(alive_pets)
#                 else:
#                     target_pet = None
#                 if target_pet:
#                     target_pet.health -= self.damage
#                     target_pet.hurt()
#         elif self.target == "all":
#             targets = []
#             # Damage the pets
#             if team:
#                 for pet in team.pets:
#                     if pet.is_alive():
#                         pet.health -= self.damage
#                         targets.append(pet)
#             if enemy_team:
#                 for pet in enemy_team.pets:
#                     if pet.is_alive():
#                         pet.health -= self.damage
#                         targets.append(pet)
#             priority_dict = prioritize_pets(targets)
#             for target in sorted(priority_dict.keys(), reverse=True):
#                 pets_with_same_priority = priority_dict[target]
#                 for pet in pets_with_same_priority:
#                     pet.hurt()
#         elif self.target == "friend_behind":
#             index = team.pets.index(pet)
#             if index < 5 and len(team.pets) > 1:
#                 target = team.pets[index + 1]
#
#                 if target:
#                     target.health -= self.damage
#                     target.hurt()
#         else:
#             print(f'{self.__class__}:{self.target} not implemented')
#
#     def trigger(self, event, *args, **kwargs):
#         if event == self.trigger_event:
#             self.apply(*args, **kwargs)


# class ModifyStatsAbility(Ability):
#     def __init__(self, attack_change, health_change, target, trigger_event, buff_length=0, scope=None, filter=None,
#                  get_best=None, reverse=False, attack_multiplier=0, health_multiplier=0):
#         self.attack_change = attack_change
#         self.health_change = health_change
#         self.target = target
#         self.trigger_event = trigger_event
#         self.buff_length = buff_length
#         self.scope = scope
#         self.get_best = get_best
#         self.reverse = reverse
#         self.filter = filter
#         self.attack_multiplier = attack_multiplier
#         self.health_multiplier = health_multiplier
#
#     def apply(self, pet, team, **kwargs):
#         if self.target == "random_friendly":
#             # Create a list of friendly pets, excluding the triggering pet
#             available_targets = [p for p in team.pets if p is not pet and p.health > 0]
#
#             # Check if there are available targets
#             if available_targets:
#                 # Choose a random pet from the available targets
#                 target_pet = choice(available_targets)
#
#                 # Modify the target pet's stats
#                 target_pet.attack += self.attack_change
#                 target_pet.health += self.health_change
#         elif self.target == "front_most_friend":
#             if team.pets:
#                 target = team.pets[0]
#                 target.attack += self.attack_change
#         elif self.target == "friend_ahead":
#             index = team.pets.index(pet)
#             pet_count = len(team.pets)
#             if index == 0:
#                 return
#
#             target = team.pets[index - 1]
#
#             if not self.scope:
#                 target.attack += self.attack_change
#                 target.health += self.health_change
#             else:  # TODO generalize for different scopes
#                 if self.scope == "self":
#                     target.attack += self.attack_multiplier * pet.attack
#                     target.health += self.health_multiplier * pet.health
#                     target.attack = math.floor(target.attack)
#                     target.health = math.floor(target.health)
#
#         elif self.target == "self":
#             if not self.scope:
#                 pet.attack += self.attack_change
#                 pet.health += self.health_change
#             else:  # TODO generalize for different scopes
#                 if self.get_best:
#                     sorted_list = sort_pets_by_attribute(team.pets, self.get_best)
#                     if sorted_list:
#                         reference = sorted_list[0]
#                         pet.attack += self.attack_multiplier * reference.attack
#                         pet.health += self.health_multiplier * reference.health
#                         pet.attack = math.floor(pet.attack)
#                         pet.health = math.floor(pet.health)
#                 elif self.filter:
#                     pet_count = 0
#                     if self.filter == "faint":
#                         if self.scope == "all_friends":
#                             for friend in team.pets:
#                                 if friend.name in pet_dict.HAS_FAINT_ABILITY:
#                                     pet_count += 1
#                             pet.attack += self.attack_multiplier * pet_count
#                             pet.health += self.health_multiplier * pet_count
#
#         elif self.target == "2_friends_behind":
#             index = team.pets.index(pet)
#             pet_count = len(team.pets)
#             if pet_count > 1:
#                 if index == pet_count - 2:
#                     behind_1 = team.pets[index + 1]
#                     behind_1.attack += self.attack_change
#                     behind_1.health += self.health_change
#                 elif pet_count - index >= 3:
#                     behind_1 = team.pets[index + 1]
#                     behind_1.attack += self.attack_change
#                     behind_1.health += self.health_change
#                     behind_2 = team.pets[index + 2]
#                     behind_2.attack += self.attack_change
#                     behind_2.health += self.health_change
#         else:
#             print(f'{self.__class__}:{self.target} not implemented')
#
#     def trigger(self, event, *args, **kwargs):
#         if event == self.trigger_event:
#             self.apply(*args, **kwargs)


