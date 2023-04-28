from abc import abstractmethod
from .ability_abstract import AbilityBase
from random import sample
import src.logger as logger

log = logger.setup_logger(__name__)


class ModifyStatsAbilityBase(AbilityBase):
    def __init__(self, owner, attack_mod, health_mod, target_type, target_n, trigger_event, until_end_of_battle=False):
        super().__init__(owner, trigger_event)
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
        log.debug(f"{self.owner} modifying {target_pet}  by {self.attack_mod} / {self.health_mod} using "
                  f"{self.__class__.__name__}")
        target_pet.attack += self.attack_mod
        target_pet.health += self.health_mod


class ModifyStatsAbilityRandomFriend(ModifyStatsAbilityBase):
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


class ModifyStatsAbilityFrontFriend(ModifyStatsAbilityBase):
    def apply(self, pet, team, **kwargs):
        if team.pets:
            target_pet = team.pets[0]
            self.add_modifiers(target_pet)


class ModifyStatsAbilityFriendBehind(ModifyStatsAbilityBase):
    def apply(self, pet, team, **kwargs):
        index = team.pets.index(pet)
        for n in range(self.target_n):
            if index >= len(team.pets)-1-n:
                return

            target = team.pets[index + 1 + n]
            self.add_modifiers(target)


class ModifyStatsAbilityFriendAhead(ModifyStatsAbilityBase):
    def apply(self, pet, team, **kwargs):
        index = team.pets.index(pet)
        if index == 0:
            return

        target = team.pets[index - 1]
        self.add_modifiers(target)
