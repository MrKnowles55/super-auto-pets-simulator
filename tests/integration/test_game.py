import unittest
from unittest.mock import MagicMock, patch

from src.pet_utils.pet import Pet
from src.action_utils.battle import Battle, Action, PriorityQueue
from src.team_utils.team import Team
from src.action_utils.signals import send_signal, Signal
from src.game_utils.game import Game

from src.data_utils.ability_enums import EffectKind, EffectTargetKind, TriggerByKind, TriggerEvent


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game(pack=None, game_mode="Normal")

        print("\n")

    @patch('src.game_utils.game.Game.generate_team')
    def test_battle_mode(self, mock_generate_team):
        self.game.battle_handler = MagicMock()
        self.game.battle_handler.battle_loop.return_value = 0

        self.assertEqual(self.game.battle_mode(), self.game.battle_handler.battle_loop())

    def test_shop_mode(self):
        pass

    @patch('src.game_utils.game.Game.generate_team')
    def test_game_loop(self, mock_generate_team):
        # Win
        self.game.battle_handler = MagicMock()
        self.game.battle_handler.battle_loop.return_value = 1

        self.game.game_loop()

        self.assertEqual(self.game.lives, 5)
        self.assertEqual(self.game.score, 10)

        # Lose
        self.setUp()
        self.game.battle_handler = MagicMock()
        self.game.battle_handler.battle_loop.return_value = -1

        self.game.game_loop()

        self.assertEqual(self.game.lives, 0)
        self.assertEqual(self.game.score, 0)

    def test_generate_team(self):
        pass

    # def test_battle(self):
    #     player0 = Pet("P0", base_attack=1, base_health=1)
    #     player1 = Pet("P1", base_attack=1, base_health=2)
    #     enemy0 = Pet("E0", base_attack=1, base_health=1)
    #     enemy1 = Pet("E1", base_attack=1, base_health=1)
    #
    #     self.game.battle_handler.player_team.add_pet(player0)
    #     self.game.battle_handler.player_team.add_pet(player1)
    #     self.game.battle_handler.enemy_team.add_pet(enemy0)
    #     self.game.battle_handler.enemy_team.add_pet(enemy1)
    #     self.game.battle_mode()
    #
    #     self.assertEqual(self.game.battle_handler.get_pet_list(), [player1])
    #     self.assertEqual(player1.health, 1)