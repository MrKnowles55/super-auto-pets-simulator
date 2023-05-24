import signals
from src.pet_data_utils.enums.trigger_event import TriggerEvent
from src.pet_data_utils.enums.trigger_by_kind import TriggerByKind
from src.pet_data_utils.enums.effect_target_kind import EffectTargetKind
from src.pet_data_utils.enums.effect_kind import EffectKind


class Pet:
    global_pet_count = 0

    def __init__(self, name, **kwargs):
        self.id = Pet.global_pet_count
        Pet.global_pet_count += 1
        # Base Stats from Template
        self.name = name
        self.base_attack = 1
        self.base_health = 1
        self.tier = 1
        self.ability = {
            "trigger": "",
            "triggered_by": "",
            "effect": "",
            "effect_dict": {}
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

        # Calculated stats
        self.attack = self.base_attack + self.attack_mod
        self.health = self.base_health + self.health_mod

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

    # Utility
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
        # TODO exception for FriendAhead overwriting EachFriend
        return self.get_relationship(signal.sender) == self.ability['triggered_by']

    # Team
    def update_position(self, new_position):
        self.position = new_position
        if self.start_position == -1:
            self.start_position = self.position

    # Signals
    def send_signal(self, message, receiver, broadcast=False):
        signals.send_signal(message, self, receiver, broadcast)
        # print(f"{self.name} sending signal {trigger} to {target}")
        # action = self.team.create_action(self, self.ability, trigger)
        # print(action)
        # self.team.send_action(action)

    def broadcast(self, message):
        print(f"{self} is broadcasting {message}")
        self.send_signal(message, self.team, broadcast=True)

    def read_signal(self, signal, broadcast):
        if not self.check_if_relevant_signal(signal):
            return
        print(f"{self} ability triggered")


        # if sender is self:
        #     print(f"{self} sent a signal to itself.")
        #     if self.ability["triggered_by"] == "Self":
        #         print(f"It is triggered by Self")
        #     else:
        #         print(f"It is not triggered")
        # else:
        #     if sender.team == self.team:
        #         print(f"{sender} sent a signal to its friend {self} on team {self.team}")
        #         if self.ability["triggered_by"] == "EachFriend":
        #             print(f"It is triggered by EachFriend")
        #         elif self.ability["triggered_by"] == "FriendAhead":
        #             if self.position > sender.position:
        #                 print(f"It is triggered by FriendAhead")
        #             else:
        #                 print(f"Friend was behind, so no trigger.")
        #         else:
        #             print(f"It is not triggered")
        #     else:
        #         print(f"{sender} sent a signal to its enemy {self} on team {self.team}")
        #         if self.ability["triggered_by"] == "EachEnemy":
        #             print(f"It is triggered by EachEnemy")
        #         else:
        #             print(f"It is not triggered")

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
    def fake_effect(**kwargs):
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
    def target_fake(**kwargs):
        return kwargs


