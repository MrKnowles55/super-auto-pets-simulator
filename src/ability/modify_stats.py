from abc import abstractmethod
from .ability import Ability
from random import sample


class ModifyStatsAbility(Ability):
    def __init__(self, owner, attack_mod, health_mod, target_type, target_n, trigger_event, until_end_of_battle=False):
        super().__init__(owner)
        self.attack_mod = attack_mod
        self.health_mod = health_mod
        self.target_type = target_type
        self.target_n = target_n
        self.trigger_event = trigger_event
        self.until_end_of_battle = until_end_of_battle

    @abstractmethod
    def apply(self, pet, team, **kwargs):
        pass

    def add_modifiers(self, target_pet):
        target_pet.attack += self.attack_mod
        target_pet.health += self.health_mod


class ModifyStatsAbilityRandomFriend(ModifyStatsAbility):
    def apply(self, pet, team, **kwargs):
        # Create a list of friendly pets, excluding the triggering pet
        available_targets = [p for p in team.pets if p is not pet and p.health > 0]
        if available_targets:
            # Choose the specified number of target pets from the available targets
            num_targets = min(len(available_targets), self.target_n)
            target_pets = sample(available_targets, num_targets)

            # Modify the target pets' stats
            for target_pet in target_pets:
                self.add_modifiers(target_pet)


class ModifyStatsAbilityFrontFriend(ModifyStatsAbility):
    def apply(self, pet, team, **kwargs):
        if team.pets:
            target_pet = team.pets[0]
            self.add_modifiers(target_pet)


class ModifyStatsAbilityFriendAhead(ModifyStatsAbility):
    def apply(self, pet, team, **kwargs):
        index = team.pets.index(pet)
        if index == 0:
            return

        target = team.pets[index - 1]
        self.add_modifiers(target)
