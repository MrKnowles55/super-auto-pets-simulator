import logging
import unittest
from unittest.mock import MagicMock, patch

from src.pet_utils.pet import Pet
from src.action_utils.battle import Battle, Action, PriorityQueue
from src.team_utils.team import Team
from src.action_utils.signals import send_signal, Signal
from src.config_utils.custom_logger import setup_logging
from src.data_utils.ability_enums import EffectKind, EffectTargetKind, TriggerByKind, TriggerEvent
from src.food import Food

setup_logging(logging.DEBUG)


class Test_Food(unittest.TestCase):
    def setUp(self) -> None:
        setup_logging(logging.DEBUG)
        self.player_team = Team("Player")
        self.enemy_team = Team("Enemy")
        self.shop_team = Team("Shop")
        self.battle = Battle(self.player_team, self.enemy_team)

        print("\n")

    def test_buy(self):
        foo = Food("Salad Bowl")
        foo.team = self.player_team
        self.player_team.add_pet(Pet("Test"))
        self.player_team.add_pet(Pet("Test"))
        self.player_team.add_pet(Pet("Test"))
        for k, v in foo.__dict__.items():
            print(k, v)

        foo.buy()

    def test_apple(self):
        foo = Food("apple")
        foo.team = self.player_team
        self.player_team.add_pet(Pet("Test Pet", base_attack=1, base_health=1, attack_mod=0, health_mod=0))
        foo.buy()
        print(self.player_team.first.combat_stats)