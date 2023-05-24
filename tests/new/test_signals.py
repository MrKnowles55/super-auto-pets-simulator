import unittest
from unittest.mock import MagicMock, patch
from pet.new_pet import Pet
from new_battle import Battle
from new_team import Team
from signals import Signal, send_signal

from src.pet_data_utils.enums.trigger_event import TriggerEvent
from src.pet_data_utils.enums.trigger_by_kind import TriggerByKind
from src.pet_data_utils.enums.effect_target_kind import EffectTargetKind
from src.pet_data_utils.enums.effect_kind import EffectKind


class TestSignal(unittest.TestCase):
    def setUp(self) -> None:
        print("\n")

    def test_send_signal(self):
        sender = MagicMock()
        receiver = MagicMock()
        message = TriggerEvent.Test
        broadcast = False

        signal = send_signal(message, sender, receiver, broadcast)

        receiver.read_signal.assert_called_once_with(
            signal, broadcast
        )


class TestSignalBroadcast(unittest.TestCase):
    def setUp(self):
        self.pet = Pet("TestPet")

        self.player_team = Team('player')
        self.enemy_team = Team('enemy')
        self.battle = Battle(self.player_team, self.enemy_team)
        self.player_team.action_handler = self.battle
        self.enemy_team.action_handler = self.battle
        print("\n")

    @patch("signals.send_signal")
    def test_broadcast_from_pet(self, mock_send_signal):
        test_message = TriggerEvent.Test

        self.pet.broadcast(test_message)

        # Verify that send_signal was called with the correct arguments.
        mock_send_signal.assert_called_with(test_message, self.pet, self.pet.team, True)

    @patch("signals.send_signal")
    def test_team_broadcast(self, mock_send_signal):
        # Setup
        sender_pet = Pet("test")
        self.player_team.add_pet(sender_pet)

        receiver_pet_1 = Pet("rec_1")
        receiver_pet_2 = Pet("rec_2")

        self.player_team.add_pet(receiver_pet_1)
        self.enemy_team.add_pet(receiver_pet_2)

        # Call the method under test
        self.player_team.read_signal(signal=MagicMock(message=TriggerEvent.Test, sender=sender_pet), broadcast=True)

        # Because the method is being mocked, the enemy_team will not actually read that it needs to broadcast,
        # so we do it manually
        self.enemy_team.read_signal(signal=MagicMock(message=TriggerEvent.Test, sender=sender_pet), broadcast=False)
        # Verify
        # It should call send_signal for each pet in the team plus once for the enemy team
        self.assertEqual(mock_send_signal.call_count,
                         len(self.player_team.pets_list) + len(self.enemy_team.pets_list) + 1)


