from abc import ABC, abstractmethod
from src.config_utils.logger import setup_logger, log_call, log_class_init

log = setup_logger(__name__)


class AbilityBase(ABC):
    def __init__(self, owner, trigger_event=None):
        self.owner = owner
        self.trigger_event = trigger_event

    @log_call(log)
    @abstractmethod
    def apply(self, **kwargs):
        return

    @log_call(log)
    def trigger(self, event, **kwargs):
        if event == self.trigger_event:
            return self.apply(**kwargs)

    def __repr__(self):
        attributes = ', '.join([f"{k}={repr(v)}" for k, v in vars(self).items()])
        # return f"{self.__class__.__name__}({attributes})"
        return f"{self.__class__.__name__}"


@log_class_init(log)
class No_Ability(AbilityBase):
    def __init__(self, owner, trigger_event=None):
        super().__init__(owner, trigger_event)

    @log_call(log)
    def apply(self, **kwargs):
        return


# class Summon(Ability):
#     def __init__(self, owner, token, trigger_event, team_to_summon_to):
#         super().__init__(owner)
#         self.token = token
#         self.trigger_event = trigger_event
#         self.team_utils = team_to_summon_to
#
#     def apply(self, pet_utils, team_utils, **kwargs):
#         from pet_factory import create_pet
#         if self.trigger_event == TriggerEvent.Faint:
#
#             index = team_utils.pets.index(pet_utils)
#
#             try:
#                 new_pet = create_pet(self.token)
#                 team_utils.remove_pet(pet_utils)
#                 team_utils.add_pet(new_pet, index)
#             except KeyError:
#                 print(f"Cannot create pet_utils of type {self.token}")
#                 team_utils.remove_pet(pet_utils)
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
#     def apply(self, pet_utils, team_utils, **kwargs):
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
#             if team_utils:
#                 for pet_utils in team_utils.pets:
#                     if pet_utils.is_alive():
#                         pet_utils.health -= self.damage
#                         targets.append(pet_utils)
#             if enemy_team:
#                 for pet_utils in enemy_team.pets:
#                     if pet_utils.is_alive():
#                         pet_utils.health -= self.damage
#                         targets.append(pet_utils)
#             priority_dict = prioritize_pets(targets)
#             for target in sorted(priority_dict.keys(), reverse=True):
#                 pets_with_same_priority = priority_dict[target]
#                 for pet_utils in pets_with_same_priority:
#                     pet_utils.hurt()
#         elif self.target == "friend_behind":
#             index = team_utils.pets.index(pet_utils)
#             if index < 5 and len(team_utils.pets) > 1:
#                 target = team_utils.pets[index + 1]
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
#     def apply(self, pet_utils, team_utils, **kwargs):
#         if self.target == "random_friendly":
#             # Create a list of friendly pets, excluding the triggering pet_utils
#             available_targets = [p for p in team_utils.pets if p is not pet_utils and p.health > 0]
#
#             # Check if there are available targets
#             if available_targets:
#                 # Choose a random pet_utils from the available targets
#                 target_pet = choice(available_targets)
#
#                 # Modify the target pet_utils's stats
#                 target_pet.attack += self.attack_change
#                 target_pet.health += self.health_change
#         elif self.target == "front_most_friend":
#             if team_utils.pets:
#                 target = team_utils.pets[0]
#                 target.attack += self.attack_change
#         elif self.target == "friend_ahead":
#             index = team_utils.pets.index(pet_utils)
#             pet_count = len(team_utils.pets)
#             if index == 0:
#                 return
#
#             target = team_utils.pets[index - 1]
#
#             if not self.scope:
#                 target.attack += self.attack_change
#                 target.health += self.health_change
#             else:  # TODO generalize for different scopes
#                 if self.scope == "self":
#                     target.attack += self.attack_multiplier * pet_utils.attack
#                     target.health += self.health_multiplier * pet_utils.health
#                     target.attack = math.floor(target.attack)
#                     target.health = math.floor(target.health)
#
#         elif self.target == "self":
#             if not self.scope:
#                 pet_utils.attack += self.attack_change
#                 pet_utils.health += self.health_change
#             else:  # TODO generalize for different scopes
#                 if self.get_best:
#                     sorted_list = sort_pets_by_attribute(team_utils.pets, self.get_best)
#                     if sorted_list:
#                         reference = sorted_list[0]
#                         pet_utils.attack += self.attack_multiplier * reference.attack
#                         pet_utils.health += self.health_multiplier * reference.health
#                         pet_utils.attack = math.floor(pet_utils.attack)
#                         pet_utils.health = math.floor(pet_utils.health)
#                 elif self.filter:
#                     pet_count = 0
#                     if self.filter == "faint":
#                         if self.scope == "all_friends":
#                             for friend in team_utils.pets:
#                                 if friend.name in pet_dict.HAS_FAINT_ABILITY:
#                                     pet_count += 1
#                             pet_utils.attack += self.attack_multiplier * pet_count
#                             pet_utils.health += self.health_multiplier * pet_count
#
#         elif self.target == "2_friends_behind":
#             index = team_utils.pets.index(pet_utils)
#             pet_count = len(team_utils.pets)
#             if pet_count > 1:
#                 if index == pet_count - 2:
#                     behind_1 = team_utils.pets[index + 1]
#                     behind_1.attack += self.attack_change
#                     behind_1.health += self.health_change
#                 elif pet_count - index >= 3:
#                     behind_1 = team_utils.pets[index + 1]
#                     behind_1.attack += self.attack_change
#                     behind_1.health += self.health_change
#                     behind_2 = team_utils.pets[index + 2]
#                     behind_2.attack += self.attack_change
#                     behind_2.health += self.health_change
#         else:
#             print(f'{self.__class__}:{self.target} not implemented')
#
#     def trigger(self, event, *args, **kwargs):
#         if event == self.trigger_event:
#             self.apply(*args, **kwargs)


