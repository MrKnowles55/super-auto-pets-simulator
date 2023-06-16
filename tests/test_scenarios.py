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


class TestScenarios(unittest.TestCase):
    def setUp(self) -> None:
        self.player_team = Team("Player")
        self.enemy_team = Team("Enemy")
        self.battle = Battle(self.player_team, self.enemy_team)
        print("\n")

    def test_mosquito_vs_ant(self):
        self.pet = Pet("Mosquito", level=2)
        self.player_team.add_pet(self.pet)
        self.enemy_team.add_pet(Pet("Ant"))
        self.enemy_team.add_pet(Pet("Ant"))
        self.enemy_team.add_pet(Pet("Ant"))

        self.battle.battle_loop()

        self.assertEqual(self.player_team.length, 0)
        self.assertEqual(self.enemy_team.length, 1)
        self.assertEqual(self.enemy_team.first.attack, 6)
        self.assertEqual(self.enemy_team.first.health, 1)

    def test_hedgehog(self):
        self.player_team.add_pet(Pet("Hedgehog"))
        self.player_team.add_pet(Pet("Hedgehog"))
        self.player_team.add_pet(Pet("Hedgehog"))

        self.enemy_team.add_pet(Pet("Test"))
        self.enemy_team.add_pet(Pet("Test"))
        self.enemy_team.add_pet(Pet("Test"))
        self.enemy_team.add_pet(Pet("Test"))
        self.enemy_team.add_pet(Pet("Test"))

        self.battle.battle_loop()

        self.assertEqual(self.player_team.length, 0)
        self.assertEqual(self.enemy_team.length, 0)

    def test_peacock(self):
        self.player_team.add_pet(Pet("Badger"))

        self.enemy_team.add_pet(Pet("Test", base_attack=10, base_health=10))

        self.battle.battle_loop()


