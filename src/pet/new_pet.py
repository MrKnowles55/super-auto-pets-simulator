

class Pet:

    def __init__(self, name, **kwargs):
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

    # Properties
    @property
    def alive(self):
        return self.health > 0

    @property
    def trigger(self):
        return self.ability.get("trigger")

    def __str__(self):
        return f"{self.name[:2]}({self.attack}/{self.health} P:({self.start_position}/{self.position}))"

    def __repr__(self):
        return f"{self.name[:2]}({self.attack}/{self.health} P:{self.position})"

    # Team
    def update_position(self, new_position):
        self.position = new_position
        if self.start_position == -1:
            self.start_position = self.position

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


