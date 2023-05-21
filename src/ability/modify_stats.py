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
    def add_modifiers(self, target_pet, **kwargs):
        return generate_modify_stats_action(self.owner, trigger_event=self.trigger_event, target_pet=target_pet, attack_mod=self.attack_mod,
                                            health_mod=self.health_mod, **kwargs)


@log_class_init(log)
class ModifyStatsAbilityRandomFriend(ModifyStatsAbilityBase):
    @log_call(log)
    def apply(self, **kwargs):
        actions = []
        # Create a list of friendly pets, excluding the triggering pet
        available_targets = [p for p in self.owner.team.pets_list if p is not self.owner and p.health > 0]
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
        actions = []
        if self.owner.team.pets_list:
            target_pet = self.owner.team.pets_list[0]
            actions.append(self.add_modifiers(target_pet))
        return actions


@log_class_init(log)
class ModifyStatsAbilityFriendBehind(ModifyStatsAbilityBase):
    @log_call(log)
    def apply(self, **kwargs):
        actions = []
        index = kwargs.get("index")
        exclude = kwargs.get("exclude", [])
        if index is None:
            index = self.owner.team.pets_list.index(self.owner)
        viable_pets = [x for x in self.owner.team.pets_list if self.owner.team.pets_list.index(x) > index and x.is_alive]
        if viable_pets:
            for n in range(self.target_n):
                if n < len(viable_pets):
                    if viable_pets[n] not in exclude:
                        target = viable_pets[n]
                        actions.append(self.add_modifiers(target, index=index, exclude=exclude))
                        exclude.append(target)
        return actions

        #     if index >= len(self.owner.team.pets_list)-1-n:
        #         return actions
        #
        #     target = self.owner.team.pets_list[index + 1 + n]
        #     actions.append(self.add_modifiers(target, index=index, exclude=exclude))
        # return actions


@log_class_init(log)
class ModifyStatsAbilityFriendAhead(ModifyStatsAbilityBase):
    @log_call(log)
    def apply(self, **kwargs):
        actions = []
        index = self.owner.team.pets_list.index(self.owner)
        if index == 0:
            return actions

        target = self.owner.team.pets_list[index - 1]
        actions.append(self.add_modifiers(target))

        return actions
