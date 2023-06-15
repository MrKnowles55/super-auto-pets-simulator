import logging
import unittest
from unittest.mock import MagicMock, patch

from src.pet_utils.pet import Pet
from src.action_utils.battle import Battle, Action, PriorityQueue
from src.team_utils.team import Team
from src.action_utils.signals import send_signal, Signal
from src.config_utils.custom_logger import setup_logging
from src.data_utils.ability_enums import EffectKind, EffectTargetKind, TriggerByKind, TriggerEvent

setup_logging(logging.DEBUG)


def fill_team(team, size):
    team.pets_list = []
    for _ in range(size):
        team.add_pet(Pet(f"{team.name[0]}"))


class TestPet_Effect(unittest.TestCase):
    def setUp(self) -> None:
        self.player_team = Team("Player")
        self.enemy_team = Team("Enemy")
        self.battle = Battle(self.player_team, self.enemy_team)

        self.pet = Pet('test')
        self.player_team.add_pet(self.pet)

        print("\n")

    # Perk
    def test_apply_status(self):
        pass

    # Damage

    def test_deal_damage(self):
        # Target Self
        # deal 1 damage, then  -1 and 0.5 damage (which round to 0)
        self.pet.base_health = 2
        self.pet.deal_damage(target=EffectTargetKind.Self, amount=1)
        self.pet.deal_damage(target=EffectTargetKind.Self, amount=-1)
        self.pet.deal_damage(target=EffectTargetKind.Self, amount=0.5)
        self.assertEqual(self.pet.health, 1)
        self.assertEqual(self.pet.damage, 1)

        # Target All
        fill_team(self.player_team, 5)
        fill_team(self.enemy_team, 5)
        self.player_team.first.deal_damage(target=EffectTargetKind.All, amount=1)
        self.assertEqual(self.player_team.length, 0)
        self.assertEqual(self.enemy_team.length, 0)

    # Food
    def test_food_multiplier(self):
        pass

    # Level and Experience

    def test_evolve(self):
        pass
        # for lvl in range(1, 4):
        #     self.assertEqual(self.pet.level, lvl)
        #     self.assertEqual(self.pet.base_health, lvl)
        #     self.assertEqual(self.pet.base_attack, lvl)
        #     self.pet.evolve(target=EffectTargetKind.Self)

    def test_gain_experience(self):

        while self.pet.level < 3:
            self.pet.gain_experience(target=EffectTargetKind.Self)

        self.assertEqual(self.pet.level, 3)
        self.assertEqual(self.pet.experience, 0)
        self.assertEqual(self.pet.base_health, 6)
        self.assertEqual(self.pet.base_attack, 6)
        self.assertEqual(self.pet.ability, self.pet.ability_by_level[3])

    # Gold and Other Currency

    def test_gain_gold(self):
        pass

    def test_roll_modifier(self):
        pass

    def test_conserve_gold(self):
        pass

    def test_gain_trumpets(self):
        pass

    # Buff / Nerf

    def test_modify_stats(self):
        self.pet.modify_stats(target=EffectTargetKind.Self, attack_mod=1)
        self.assertEqual(self.pet.attack_mod, 1)

        for mod in range(-2, 1):
            self.pet.attack_mod = 0
            self.pet.health_mod = 0
            self.pet.modify_stats(target=EffectTargetKind.Self, attack_mod=mod, health_mod=mod)
            self.assertEqual(self.pet.attack, 1+mod)
            self.assertEqual(self.pet.health, max(1+mod, 1))

    def test_reduce_health(self):
        test_healths = [1, 2, 3, 5, 10, 39, 50]
        expected_healths = {1: [1, 1, 1], 2: [1, 1, 1], 3: [2, 1, 1], 5: [3, 1, 1], 10: [6, 3, 1], 39: [26, 13, 1], 50: [33, 17, 1]}
        for health in test_healths:
            self.pet.base_health = health
            for i, percent in enumerate([33, 66, 100]):
                self.pet.health_mod = 0
                self.pet.reduce_health(target=EffectTargetKind.Self, health_mod=percent)
                self.assertEqual(self.pet.health, expected_healths[health][i])

    # Shop

    def test_refill_shops(self):
        pass

    def test_discount_food(self):
        pass

    def test_modify_shop(self):
        pass

    # Transfer

    def test_repeat_ability(self):
        pass

    def test_transfer_stats(self):
        pass

    def test_transfer_ability(self):
        pass

    def test_steal_food(self):
        pass

    # Summon

    def test_summon_pet(self):
        pass

    # Special

    def test_swallow(self):
        pass

    def test_move(self):
        pass

    def test_activate_ability(self):
        pass