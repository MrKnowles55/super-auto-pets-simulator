import unittest
from unittest.mock import MagicMock, patch

from src.pet_utils.pet import Pet
from src.action_utils.battle import Battle, Action, PriorityQueue
from src.team_utils.team import Team
from src.action_utils.signals import send_signal, Signal
from src.game_utils.game import Game

from src.data_utils.enums.trigger_event import TriggerEvent
from src.data_utils.enums.trigger_by_kind import TriggerByKind
from src.data_utils.enums.effect_target_kind import EffectTargetKind
from src.data_utils.enums.effect_kind import EffectKind


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()

        print("\n")

    def test_battle(self):
        player0 = Pet("P0", base_attack=1, base_health=1)
        player1 = Pet("P1", base_attack=1, base_health=2)
        enemy0 = Pet("E0", base_attack=1, base_health=1)
        enemy1 = Pet("E1", base_attack=1, base_health=1)

        self.game.battle_handler.player_team.add_pet(player0)
        self.game.battle_handler.player_team.add_pet(player1)
        self.game.battle_handler.enemy_team.add_pet(enemy0)
        self.game.battle_handler.enemy_team.add_pet(enemy1)
        self.game.battle_mode()

        self.assertEqual(self.game.battle_handler.get_pet_list(), [player1])
        self.assertEqual(player1.health, 1)