import copy
import random
import re
from math import floor

from src.action_utils import signals
from src.config_utils.custom_logger import get_custom_logger
from src.data_utils.ability_enums import EffectKind, EffectTargetKind, TriggerByKind, TriggerEvent
from src.data_utils.pet_data_manager import pet_db

logger = get_custom_logger(__name__)


class Pet:
    global_pet_count = 0

    def __init__(self, name, **kwargs):
        self.id = Pet.global_pet_count
        Pet.global_pet_count += 1

        self.name = name.title()
        template = pet_db.pet_dict.get(self.database_id, pet_db.pet_dict.get("pet-default"))
        # Base Stats from Template
        self.base_attack = template.get('base_attack', 1)
        self.base_health = template.get('base_health', 1)
        self.tier = template.get('tier', 1)

        self.ability_by_level = {
            1: self.translate_ability_data(template.get("level_1_ability", {})),
            2: self.translate_ability_data(template.get("level_2_ability", {})),
            3: self.translate_ability_data(template.get("level_3_ability", {}))
        }

        # Default assumed parameters
        self.level = 1
        self.experience = 0
        self.attack_mod = 0
        self.health_mod = 0
        self.damage = 0

        # Team parameters
        self.team = None
        self.start_position = -1
        self.position = -1
        # set additional attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}_{self.id}"

    # Properties

    @property
    def attack(self):
        return min(self.base_attack + self.attack_mod, 50)

    @property
    def health(self):
        return min(self.base_health + self.health_mod - self.damage, 50)

    @property
    def ability(self):
        return self.ability_by_level[self.level]

    @property
    def alive(self):
        return self.health > 0

    @property
    def trigger(self):
        return self.ability.get("trigger")

    @property
    def triggered_by(self):
        return self.ability.get("triggered_by")

    @property
    def database_id(self):
        return "pet-" + self.name.lower().replace(" ", "-")

    @property
    def combat_stats(self):
        return f"{self.attack}/{self.health}"

    @property
    def combat_stats_full(self):
        return f"({self.base_attack}+{self.attack_mod}={self.attack}/{self.base_health}+{self.health_mod}-{self.damage}={self.health})"

    # Utility
    def translate_ability_data(self, template_data):
        ability_data = copy.deepcopy(template_data)
        if not ability_data:
            return {}
        trigger = self._string_to_enum(ability_data.get("trigger"), TriggerEvent)
        triggered_by = self._string_to_enum(ability_data.get("triggered_by"), TriggerByKind)
        effect = self._string_to_enum(ability_data.get("effect").get("kind"), EffectKind)
        # target = self._string_to_enum(ability_data.get("effect").get("target"), EffectTargetKind)
        target = self._string_to_enum(ability_data.get("effect", {}).get("target", {}).get("kind", {}), EffectTargetKind)
        pet_from = self._string_to_enum(ability_data.get("effect", {}).get("from", {}).get("kind", {}), EffectTargetKind)
        pet_to = self._string_to_enum(ability_data.get("effect", {}).get("to", {}).get("kind", {}),
                                        EffectTargetKind)
        ability_data["trigger"] = trigger
        ability_data["triggered_by"] = triggered_by
        ability_data["effect"]["kind"] = effect
        if target:
            ability_data["effect"]["n"] = ability_data["effect"]["target"].get("n")
            ability_data["effect"]["target"] = target
        if pet_from:
            ability_data["effect"]["from"]["kind"] = pet_from
        if pet_to:
            ability_data["effect"]["to"]["kind"] = pet_to

        return ability_data

    @staticmethod
    def _string_to_enum(input_string, enum):
        if isinstance(input_string, enum):
            return input_string
        for item in enum:
            if item.name == input_string:
                return item
        return None

    def _enum_to_string(self, enum):
        words = re.findall('[A-Z][^A-Z]*', enum.name)
        words = [word.lower() for word in words]
        return "_".join(words)

    def get_relationship(self, pet):
        if not isinstance(pet, Pet):
            return TriggerByKind.Player
        if pet is self:
            return TriggerByKind.Self

        if pet in self.team.pets_list:
            if pet.position < self.position:
                return TriggerByKind.FriendAhead
            else:
                return TriggerByKind.EachFriend
        else:
            return TriggerByKind.EachEnemy

    def check_if_triggered(self, trigger):
        return self.ability["trigger"] == trigger

    def check_if_relevant_signal(self, signal):
        relationship = self.get_relationship(signal.sender)
        looking_for = self.ability['triggered_by']
        # FriendAhead is also EachFriend, otherwise compare directly.
        if looking_for == TriggerByKind.EachFriend and relationship == TriggerByKind.FriendAhead:
            return True
        else:
            return relationship == looking_for

    # Combat
    def attack_pet(self, opponent):
        logger.debug(f"{self}({self.combat_stats}) attack {opponent}{opponent.combat_stats}")
        opponent._damage(self.attack)

    def update(self):
        # Check for Level up
        if (self.experience >= 2 and self.level == 1) or (self.experience >= 3 and self.level == 2):
            self.level_up()
        # Check for Faint
        if not self.alive:
            self.faint()

    # Team
    def update_position(self, new_position):
        self.position = new_position
        if self.start_position == -1:
            self.start_position = self.position

    # Signals
    def send_signal(self, message, receiver, broadcast=False):
        signals.send_signal(message, self, receiver, broadcast)

    def broadcast(self, message):
        self.send_signal(message, self.team, broadcast=True)

    def read_signal(self, signal, broadcast=False):
        if not self.check_if_relevant_signal(signal):
            return
        # method = self._enum_to_string(self.ability["effect"]["kind"])
        # getattr(self, method)()
        action = self.team.create_action(pet=self, ability_dict=self.ability, trigger=self.trigger)
        self.team.send_action(action)

    def faint(self):
        logger.debug(f"{self} fainted.")
        self.broadcast(TriggerEvent.Faint)
        # TODO fix
        self.team.remove_pet(self)

    def hurt(self):
        logger.debug(f"{self} was hurt.")
        self.broadcast(TriggerEvent.Hurt)

    def _damage(self, amount):
        self.damage += amount
        self.hurt()

    def level_up(self):
        self.experience = 0
        self.level += 1
        logger.debug(f"{self} leveled up {self.level}")

    ############################################################
    # Ability Effects : Called when an Action is executed.     #
    ############################################################

    def _get_target(self, **kwargs):
        return getattr(self, 'target_'+self._enum_to_string(kwargs.get("target")))(**kwargs)

    def _get_to(self, **kwargs):
        return getattr(self, 'target_'+self._enum_to_string(kwargs.get("to", {}).get("kind"),))(**kwargs)

    def _get_from(self, **kwargs):
        return getattr(self, 'target_'+self._enum_to_string(kwargs.get("from", {}).get("kind")))(**kwargs)

    # Perk

    @staticmethod
    def apply_status(**kwargs):
        # ['kind', 'status', 'target_kind', 'to_kind', 'to_n']
        return kwargs

    # Damage

    def deal_damage(self, **kwargs):
        targets = self._get_target(**kwargs)
        amount = kwargs.get("amount", 0)
        if isinstance(amount, dict):
            percentage = kwargs.get("amount").get('attack_damage_percent', 0)
            amount = floor(self.attack * percentage / 100)
        else:
            amount = floor(max(kwargs.get("amount", 0), 0))
        logger.debug(f"{self} deal_damage to {targets} using {kwargs}")
        for target in targets:
            target._damage(amount)
            target.update()

    # Food

    @staticmethod
    def food_multiplier(**kwargs):
        # amount
        return kwargs

    # Level and Experience

    def gain_experience(self, **kwargs):
        targets = self._get_target(**kwargs)
        logger.debug(f"{self} gave {targets} exp using {kwargs}")
        for target in targets:
            target.experience += 1
            target.base_health += 1
            target.base_attack += 1
            target.update()

    # Gold and Other Currency

    @staticmethod
    def gain_gold(**kwargs):
        # amount
        return kwargs

    @staticmethod
    def roll_modifier(**kwargs):
        return kwargs

    @staticmethod
    def conserve_gold(**kwargs):
        return kwargs

    @staticmethod
    def gain_trumpets(**kwargs):
        return kwargs

    # Buff / Nerf

    @staticmethod
    def _add_stats(target, attack_mod, health_mod):
        target.attack_mod += attack_mod
        target.health_mod += health_mod

    @staticmethod
    def _multiply(value, percent):
        output = value * percent / 100
        if output == 0.99:
            output = 1
        return floor(output)

    @staticmethod
    def _divide(value, percent):
        return floor(value * (100 - percent) / 100)

    def _multiply_stats(self, target, attack_percent=100, health_percent=100, divide=False):
        attack_percent = attack_percent / 100
        health_percent = health_percent / 100
        if divide:
            final_attack = target.attack * (1 - attack_percent)
            final_health = target.health * (1 - health_percent)
        else:
            final_attack = target.attack * (1 + attack_percent)
            final_health = target.health * (1 + health_percent)
        final_attack = max(final_attack, 0)
        final_health = max(final_health, 1)
        target.attack_mod = int(final_attack-target.base_attack)
        target.health_mod = int(final_health - target.base_health + target.damage)


    def _prevent_death_from_stat_change(self, target):
        if target.health <= 0:
            target.health_mod = 1 - target.base_health + target.damage

    def modify_stats(self, **kwargs):
        targets = self._get_target(**kwargs)
        attack_mod = kwargs.get("attack_mod", 0)
        health_mod = kwargs.get("health_mod", 0)
        until_end_of_battle = kwargs.get("until_end_of_battle ", False)

        logger.debug(f"{self} gave {targets} {'+' if attack_mod >= 0 else ''}{attack_mod}/{'+' if health_mod >= 0 else ''}{health_mod} {kwargs}")
        for target in targets:
            self._add_stats(target, attack_mod, health_mod)
            self._prevent_death_from_stat_change(target)
            target.update()

    def reduce_health(self, **kwargs):
        # Need to test how rounding works in game
        targets = self._get_target(**kwargs)
        health_mod = kwargs.get("health_mod", 100)
        logger.debug(f"{self} gave {targets} {'+' if health_mod >= 0 else ''}{health_mod} {kwargs}")
        for target in targets:
            self._multiply_stats(target, health_percent=health_mod, divide=True)
            target.update()


    # Shop

    @staticmethod
    def refill_shops(**kwargs):
        return kwargs

    @staticmethod
    def discount_food(**kwargs):
        # amount
        return kwargs

    @staticmethod
    def modify_shop(**kwargs):
        return kwargs

    # Transfer

    @staticmethod
    def repeat_ability(**kwargs):
        # ['kind', 'level', 'target_kind']
        return kwargs

    def transfer_stats(self, **kwargs):
        copy_attack = kwargs.get("copy_attack", False)
        copy_health = kwargs.get("copy_health", False)
        percentage = kwargs.get("percentage", 0)
        pet_from = self._get_from(**kwargs)[0]
        pet_to = self._get_to(**kwargs)

        attack_mod = self._multiply(pet_from.attack, percentage) * copy_attack
        health_mod = self._multiply(pet_from.health, percentage) * copy_health

        logger.debug(f"{pet_from} gave {pet_to} {'+' if attack_mod >= 0 else ''}{attack_mod}/{'+' if health_mod >= 0 else ''}{health_mod} {kwargs}")

        for target in pet_to:
            self._add_stats(target, attack_mod=attack_mod, health_mod=health_mod)
            target.update()

    @staticmethod
    def transfer_ability(**kwargs):
        # ['from_kind', 'from_n', 'kind', 'level', 'to_kind']
        return kwargs

    @staticmethod
    def steal_food(**kwargs):
        return kwargs

    # Summon

    @staticmethod
    def summon_pet(**kwargs):
        # ['base_attack', 'base_health', 'kind', 'level', 'n', 'pet', 'team']
        # Summon random ['base_attack', 'base_health', 'kind', 'level', 'tier']
        return kwargs

    # Special

    def evolve(self, **kwargs):
        # into
        pass

    @staticmethod
    def swallow(**kwargs):
        # ['kind', 'target_kind', 'target_n']
        return kwargs

    @staticmethod
    def move(**kwargs):
        return kwargs

    @staticmethod
    def activate_ability(**kwargs):
        return kwargs

    def test_effect(self, **kwargs):
        logger.debug(f"{self} test_effect")

    #######################
    # Targeting Functions #
    #######################

    # Friends
    def target_adjacent_friends(self, **kwargs):
        possible_targets = self.team.pets_list
        n = min(kwargs.get("n", 1), len(possible_targets)-1)
        origin = possible_targets.index(self)

        start = max(0, origin - n)  # Ensure start is not less than 0
        end = min(len(possible_targets), origin + n + 1)  # Ensure end is not more than length of list
        targets = possible_targets[start:origin] + possible_targets[origin + 1:end]
        return targets

    def target_different_tier_animals(self, **kwargs):
        # Should be friends not animals
        possible_targets = [pet for pet in self.team.pets_list if pet != self]
        pets_by_tier = {i: [] for i in range(1, 7)}
        for pet in possible_targets:
            pets_by_tier[pet.tier].append(pet)

        # Sample one pet from each tier
        targets = [random.choice(pets_by_tier[tier]) for tier in pets_by_tier if pets_by_tier[tier]]

        return targets

    def target_each_friend(self, **kwargs):
        return [pet for pet in self.team.pets_list if pet != self]

    def target_friend_ahead(self, **kwargs):
        n = kwargs.get("n", 1)
        index = self.team.pets_list.index(self)  # Get index of self in list
        start = max(0, index - n)  # Make sure the start index isn't negative
        return self.team.pets_list[start:index][::-1]  # Slice and reverse the list

    def target_friend_behind(self, **kwargs):
        n = kwargs.get("n", 1)
        index = self.team.pets_list.index(self)  # Get index of self in list
        end = min(len(self.team.pets_list),
                  index + n + 1)  # Make sure the end index doesn't exceed the length of the list
        return self.team.pets_list[index + 1:end]  # Slice the list

    def target_level2_and_3_friends(self, **kwargs):
        possible_targets = [pet for pet in self.team.pets_list if pet != self and pet.level != 1]
        n = min(kwargs.get("n", 1), len(possible_targets))
        return random.sample(possible_targets, n)

    def target_random_friend(self, **kwargs):
        possible_targets = [pet for pet in self.team.pets_list if pet != self]
        n = min(kwargs.get("n", 1), len(possible_targets))
        targets = random.sample(possible_targets, n)
        return targets

    def target_right_most_friend(self, **kwargs):
        return [self.team.pets_list[0]]

    # Enemies
    def target_each_enemy(self, **kwargs):
        return self.team.other_team.pets_list

    def target_first_enemy(self, **kwargs):
        return [self.team.other_team.pets_list[0]]

    def target_highest_health_enemy(self, **kwargs):
        return [sorted(self.team.other_team.pets_list, key=lambda x: x.health, reverse=True)[0]]

    def target_lowest_health_enemy(self, **kwargs):
        return [sorted(self.team.other_team.pets_list, key=lambda x: x.health, reverse=False)[0]]

    def target_last_enemy(self, **kwargs):
        return [self.team.other_team.pets_list[-1]]

    def target_random_enemy(self, **kwargs):
        possible_targets = self.team.other_team.pets_list
        n = min(kwargs.get("n", 1), len(possible_targets))
        targets = random.sample(possible_targets, n)
        return targets

    # Shop

    # @staticmethod
    # def target_each_shop_animal(**kwargs):
    #     return kwargs
    #
    # @staticmethod
    # def target_left_most_shop_animal(**kwargs):
    #     return kwargs

    # Other
    def target_self(self, **kwargs):
        return [self]

    def target_all(self, **kwargs):
        # only used for faint abilities, may need to remove self from targets
        return self.team.pets_list + self.team.other_team.pets_list

    def target_adjacent_animals(self, **kwargs):
        possible_targets = self.team.pets_list[::-1] + self.team.other_team.pets_list
        n = min(kwargs.get("n", 1), len(possible_targets)-1)
        origin = possible_targets.index(self)

        start = max(0, origin - n)  # Ensure start is not less than 0
        end = min(len(possible_targets), origin + n + 1)  # Ensure end is not more than length of list
        targets = possible_targets[start:origin] + possible_targets[origin + 1:end]

        return targets

    @staticmethod
    def target_triggering_entity(**kwargs):
        return [kwargs.get("triggering_entity", None)]

    @staticmethod
    def target_test_target(**kwargs):
        return [kwargs]


if __name__ == "__main__":
    x = Pet("Test Pet")

    for lvl, ability in x.ability_by_level.items():
        print(lvl)
        for key, item in ability.items():
            print("\t", key, item)
