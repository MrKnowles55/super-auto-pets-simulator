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

    def test_create_action(self):
        # Check triggered ability
        ability = {"trigger": TriggerEvent.TestTrigger, "effect_dict": {}}
        pet = MagicMock(ability=ability)

        action = self.battle.create_action(pet, pet.ability, TriggerEvent.TestTrigger)
        self.assertEqual(action.__dict__, {"pet": pet, "method": None, "kwargs": {}})

        # Check ability not triggered
        action = self.battle.create_action(pet, pet.ability, None)
        self.assertFalse(action)

    def test_enqueue(self):
        action = MagicMock()
        priority = 0

        self.battle.enqueue(priority, action)

        self.assertEqual(self.battle.action_queue.queue, [(0, 0.0, action)])

    def test_start_of_battle(self):
        ability = {"trigger": TriggerEvent.StartOfBattle, "effect_dict": {}}
        pet0 = MagicMock(ability=ability, attack=1)
        pet1 = MagicMock(ability=ability, attack=1)
        self.battle.player_team.pets_list = [pet0]
        self.battle.enemy_team.pets_list = [pet1]

        self.battle.start_of_battle()
        self.assertEqual(len(self.battle.action_queue), 2)

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


