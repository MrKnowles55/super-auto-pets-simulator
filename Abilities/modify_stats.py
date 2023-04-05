from abilities import Ability
from random import choice


class ModifyStatsAbility(Ability):
    def __init__(self, owner, attack_mod, health_mod, target_type, target_n, trigger_event, until_end_of_battle=False):
        super().__init__(owner)
        self.attack_mod = attack_mod
        self.health_mod = health_mod
        self.target_type = target_type
        self.target_n = target_n
        self.trigger_event = trigger_event
        self.until_end_of_battle = until_end_of_battle


class ModifyStatsAbilityRandomFriend(ModifyStatsAbility):
    def apply(self, pet, team, **kwargs):
        # Create a list of friendly pets, excluding the triggering pet
        available_targets = [p for p in team.pets if p is not pet and p.health > 0]
        if available_targets:
            # Choose a random pet from the available targets
            target_pet = choice(available_targets)

            # Modify the target pet's stats
            target_pet.attack += self.attack_mod
            target_pet.health += self.health_mod
