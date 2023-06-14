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


def test_fill_team(team, size):
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
        # deal 1 damage, then  -1 and 0.5 damage (which round to 0)
        self.pet.base_health = 2
        self.pet.deal_damage(target=EffectTargetKind.Self, amount=1)
        self.pet.deal_damage(target=EffectTargetKind.Self, amount=-1)
        self.pet.deal_damage(target=EffectTargetKind.Self, amount=0.5)
        self.assertEqual(self.pet.health, 1)
        self.assertEqual(self.pet.damage, 1)


    # Food

    def test_food_multiplier(self):
        pass

    # Level and Experience

    def test_evolve(self):
        pass

    def test_gain_experience(self):
        pass

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
        pass

    def test_reduce_health(self):
        pass

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