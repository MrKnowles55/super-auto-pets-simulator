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

    def test_combat(self):
        pet0 = Pet("0")
        pet1 = Pet("1")
        self.battle.player_team.add_pet(pet0)
        self.battle.enemy_team.add_pet(pet1)

        self.battle.combat()

        self.assertEqual(pet0.health, 0)
        self.assertEqual(pet1.health, 0)
        self.assertFalse(pet0.alive)

    def test_before_combat(self):
        pass

    def test_during_combat(self):
        pass

    def test_after_combat(self):
        pass

    def test_fight_loop(self):
        pass

    def test_battle_loop(self):
        # 1v1 with player pet surviving
        pet0 = Pet("0", base_health=50)
        pet1 = Pet("1", base_health=2)
        self.battle.player_team.add_pet(pet0)
        self.battle.enemy_team.add_pet(pet1)

        self.battle.battle_loop()
        self.assertEqual(pet0.health, pet0.base_health-pet1.attack*2)

        # 5v5 with single survivor
        self.battle.player_team.pets_list = []
        self.battle.enemy_team.pets_list = []
        for _ in range(5):
            self.battle.player_team.add_pet(Pet(f"P{_}", base_attack=1, base_health=1))
            self.battle.enemy_team.add_pet(Pet(f"E{_}", base_attack=1, base_health=1))
        self.battle.player_team.pets_list[4].health_mod = 1

        self.battle.battle_loop()



