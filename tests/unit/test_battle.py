import unittest
from unittest.mock import MagicMock, patch

from src.action_utils.battle import Battle
from src.team_utils.team import Team

from src.data_utils.enums.trigger_event import TriggerEvent
from src.data_utils.enums.trigger_by_kind import TriggerByKind
from src.data_utils.enums.effect_target_kind import EffectTargetKind
from src.data_utils.enums.effect_kind import EffectKind


class TestBattle(unittest.TestCase):
    def setUp(self) -> None:

        player_team = MagicMock(name="Player", pets_list=[])
        enemy_team = MagicMock(name="Enemy", pets_list=[])
        self.battle = Battle(player_team, enemy_team)
        self.battle.action_queue = MagicMock()
        print("\n")

    def test_get_pet_list(self):
        self.battle.player_team.pets_list = [1, 2, 3]
        self.battle.enemy_team.pets_list = ["a", "b", "c"]

        self.assertEqual(self.battle.pets_list, [1, 2, 3, "a", "b", "c"])

