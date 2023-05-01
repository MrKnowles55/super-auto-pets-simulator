from abc import abstractmethod
from .ability_abstract import AbilityBase
from src.action.action_utils import generate_modify_stats_action
from random import sample
from src.config_utils.logger import setup_logger, log_call, log_class_init

log = setup_logger(__name__)


class ModifyStatsAbilityBase(AbilityBase):
    def __init__(self, owner, attack_mod, health_mod, target_type, target_n, trigger_event, until_end_of_battle=False):
        super().__init__(owner, trigger_event)
        self.attack_mod = attack_mod
        self.health_mod = health_mod
        self.target_type = target_type
        self.target_n = target_n
        self.trigger_event = trigger_event
        self.until_end_of_battle = until_end_of_battle

    @log_call(log)
    @abstractmethod
    def apply(self, **kwargs):
        pass

    @log_call(log)
    def add_modifiers(self, target_pet):
        return generate_modify_stats_action(self.owner, trigger_event=self.trigger_event, target_pet=target_pet, attack_mod=self.attack_mod,
                                            health_mod=self.health_mod)


@log_class_init(log)
class ModifyStatsAbilityRandomFriend(ModifyStatsAbilityBase):
    @log_call(log)
    def apply(self, **kwargs):
        actions = []
        # Create a list of friendly pets, excluding the triggering pet
        available_targets = [p for p in self.owner.team.pets if p is not self.owner and p.health > 0]
        if available_targets:
            # Choose the specified number of target pets from the available targets
            num_targets = min(len(available_targets), self.target_n)
            target_pets = sample(available_targets, num_targets)

            # Modify the target pets' stats
            for target_pet in target_pets:
                actions.append(self.add_modifiers(target_pet))

        return actions


@log_class_init(log)
class ModifyStatsAbilityFrontFriend(ModifyStatsAbilityBase):
    @log_call(log)
    def apply(self, **kwargs):
        if self.owner.team.pets:
            target_pet = self.owner.team.pets[0]
            self.add_modifiers(target_pet)


@log_class_init(log)
class ModifyStatsAbilityFriendBehind(ModifyStatsAbilityBase):
    @log_call(log)
    def apply(self, **kwargs):
        index = self.owner.team.pets.index(self.owner)
        for n in range(self.target_n):
            if index >= len(self.owner.team.pets)-1-n:
                return

            target = self.owner.team.pets[index + 1 + n]
            self.add_modifiers(target)


@log_class_init(log)
class ModifyStatsAbilityFriendAhead(ModifyStatsAbilityBase):
    @log_call(log)
    def apply(self, **kwargs):
        index = self.owner.team.pets.index(self.owner)
        if index == 0:
            return

        target = self.owner.team.pets[index - 1]
        self.add_modifiers(target)
