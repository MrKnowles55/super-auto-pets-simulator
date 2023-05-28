import unittest
from unittest.mock import MagicMock, patch

from src.pet_utils.pet import Pet
from src.action_utils.battle import Battle, Action, PriorityQueue
from src.team_utils.team import Team
from src.action_utils.signals import send_signal, Signal

from src.data_utils.enums.trigger_event import TriggerEvent
from src.data_utils.enums.trigger_by_kind import TriggerByKind
from src.data_utils.enums.effect_target_kind import EffectTargetKind
from src.data_utils.enums.effect_kind import EffectKind


class TestBattle(unittest.TestCase):
    def setUp(self) -> None:
        player_team = Team("Player")
        enemy_team = Team("Enemy")
        self.battle = Battle(player_team, enemy_team)

        print("\n")

    def test_pet_sending_action_to_queue(self):
        pet = Pet("TestPet")
        pet.team = self.battle.player_team
        pet.ability["triggered_by"] = TriggerByKind.Self
        signal = Signal(TriggerEvent.TestTrigger, pet, pet)

        expected_pet = pet
        expected_method = EffectKind.TestEffect
        expected_kwargs = {"target": EffectTargetKind.TestTarget}

        pet.read_signal(signal)
        queued_action = self.battle.action_queue.queue[0][2]

        self.assertEqual(queued_action.pet, expected_pet)
        self.assertEqual(queued_action.method, expected_method)
        self.assertEqual(queued_action.kwargs, expected_kwargs)


