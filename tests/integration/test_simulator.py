import unittest
from unittest.mock import MagicMock, patch

from src.pet_utils.pet import Pet
from src.action_utils.battle import Battle, Action, PriorityQueue
from src.team_utils.team import Team
from src.action_utils.signals import send_signal, Signal
from src.game_utils.game import Game
from src.main import Simulator

from data_utils.ability_enums import EffectKind, EffectTargetKind, TriggerByKind, TriggerEvent


class TestSimulator(unittest.TestCase):
    def setUp(self) -> None:
        self.sim = Simulator()

        print("\n")