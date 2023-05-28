import re

from src.action_utils import signals
from src.data_utils.pet_data_manager import pet_db

from src.data_utils.enums.trigger_event import TriggerEvent
from src.data_utils.enums.trigger_by_kind import TriggerByKind
from src.data_utils.enums.effect_target_kind import EffectTargetKind
from src.data_utils.enums.effect_kind import EffectKind


class Pet:
    global_pet_count = 0

    def __init__(self, name, **kwargs):
        self.id = Pet.global_pet_count
        Pet.global_pet_count += 1

        self.name = name.title()
        template = pet_db.pet_dict.get(self.database_id)
        if not template:
            print(f"No pet found called {name}. Using Default template.")
            template = pet_db.pet_dict.get("pet-default")
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
        self.attack_mod = 0
        self.health_mod = 0

        # Team parameters
        self.team = None
        self.start_position = -1
        self.position = -1

        # set additional attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Dependant Variables
        self.attack = self.base_attack + self.attack_mod
        self.health = self.base_health + self.health_mod
        self.ability = self.ability_by_level[self.level]

    def __str__(self):
        return f"{self.name}_{self.id}"

    def __repr__(self):
        return f"{self.name}_{self.id}({self.attack}/{self.health}/{self.position})"

    # Properties
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

    # Utility
    def translate_ability_data(self, template_data):
        ability_data = dict(template_data)
        trigger = self._string_to_enum(ability_data.get("trigger"), TriggerEvent)
        triggered_by = self._string_to_enum(ability_data.get("triggered_by"), TriggerByKind)
        effect = self._string_to_enum(ability_data.get("effect").get("kind"), EffectKind)
        target = self._string_to_enum(ability_data.get("effect").get("target"), EffectTargetKind)
        ability_data["trigger"] = trigger
        ability_data["triggered_by"] = triggered_by
        ability_data["effect"]["kind"] = effect
        ability_data["effect"]["target"] = target
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

    # Team
    def update_position(self, new_position):
        self.position = new_position
        if self.start_position == -1:
            self.start_position = self.position

    # Signals
    def send_signal(self, message, receiver, broadcast=False):
        signals.send_signal(message, self, receiver, broadcast)
        # print(f"{self.name} sending signal {trigger} to {target}")
        # action_utils = self.team_utils.create_action(self, self.ability, trigger)
        # print(action_utils)
        # self.team_utils.send_action(action_utils)

    def broadcast(self, message):
        print(f"{self} is broadcasting {message}")
        self.send_signal(message, self.team, broadcast=True)

    def read_signal(self, signal):
        if not self.check_if_relevant_signal(signal):
            return
        # method = self._enum_to_string(self.ability["effect"]["kind"])
        # getattr(self, method)()
        action = self.team.create_action(pet=self, ability_dict=self.ability, trigger=self.trigger)
        self.team.send_action(action)

    def faint(self):
        pass

    def hurt(self):
        pass

    # Effects

    @staticmethod
    def apply_status(**kwargs):
        return kwargs

    @staticmethod
    def deal_damage(**kwargs):
        return kwargs

    @staticmethod
    def discount_food(**kwargs):
        return kwargs

    @staticmethod
    def evolve(**kwargs):
        return kwargs

    @staticmethod
    def food_multiplier(**kwargs):
        return kwargs

    @staticmethod
    def gain_experience(**kwargs):
        return kwargs

    @staticmethod
    def gain_gold(**kwargs):
        return kwargs

    @staticmethod
    def modify_stats(**kwargs):
        return kwargs

    @staticmethod
    def reduce_health(**kwargs):
        return kwargs

    @staticmethod
    def refill_shops(**kwargs):
        return kwargs

    @staticmethod
    def repeat_ability(**kwargs):
        return kwargs

    @staticmethod
    def summon_pet(**kwargs):
        return kwargs

    @staticmethod
    def swallow(**kwargs):
        return kwargs

    @staticmethod
    def transfer_ability(**kwargs):
        return kwargs

    @staticmethod
    def transfer_stats(**kwargs):
        return kwargs

    @staticmethod
    def roll_modifier(**kwargs):
        return kwargs

    @staticmethod
    def modify_shop(**kwargs):
        return kwargs

    @staticmethod
    def conserve_gold(**kwargs):
        return kwargs

    @staticmethod
    def steal_food(**kwargs):
        return kwargs

    @staticmethod
    def gain_trumpets(**kwargs):
        return kwargs

    @staticmethod
    def move(**kwargs):
        return kwargs

    @staticmethod
    def activate_ability(**kwargs):
        return kwargs

    @staticmethod
    def test_effect(**kwargs):
        return kwargs

    # Target

    @staticmethod
    def target_adjacent_animals(**kwargs):
        return kwargs

    @staticmethod
    def target_adjacent_friends(**kwargs):
        return kwargs

    @staticmethod
    def target_all(**kwargs):
        return kwargs

    @staticmethod
    def target_different_tier_animals(**kwargs):
        return kwargs

    @staticmethod
    def target_each_enemy(**kwargs):
        return kwargs

    @staticmethod
    def target_each_friend(**kwargs):
        return kwargs

    @staticmethod
    def target_each_shop_animal(**kwargs):
        return kwargs

    @staticmethod
    def target_first_enemy(**kwargs):
        return kwargs

    @staticmethod
    def target_friend_ahead(**kwargs):
        return kwargs

    @staticmethod
    def target_friend_behind(**kwargs):
        return kwargs

    @staticmethod
    def target_highest_health_enemy(**kwargs):
        return kwargs

    @staticmethod
    def target_last_enemy(**kwargs):
        return kwargs

    @staticmethod
    def target_left_most_friend(**kwargs):
        return kwargs

    @staticmethod
    def target_level2_and_3_friends(**kwargs):
        return kwargs

    @staticmethod
    def target_lowest_health_enemy(**kwargs):
        return kwargs

    @staticmethod
    def target_random_enemy(**kwargs):
        return kwargs

    @staticmethod
    def target_random_friend(**kwargs):
        return kwargs

    @staticmethod
    def target_right_most_friend(**kwargs):
        return kwargs

    @staticmethod
    def target_self(**kwargs):
        return kwargs

    @staticmethod
    def target_triggering_entity(**kwargs):
        return kwargs

    @staticmethod
    def target_left_most_shop_animal(**kwargs):
        return kwargs

    @staticmethod
    def target_test_target(**kwargs):
        return kwargs


if __name__ == "__main__":
    x = Pet("asdasd")
    for lvl, ability in x.ability_by_level.items():
        print(lvl, ":", ability)
