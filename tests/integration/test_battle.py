import unittest
from unittest.mock import MagicMock, patch

from src.pet_utils.pet import Pet
from src.action_utils.battle import Battle, Action, PriorityQueue
from src.team_utils.team import Team
from src.action_utils.signals import send_signal, Signal

from src.data_utils.ability_enums import EffectKind, EffectTargetKind, TriggerByKind, TriggerEvent


class TestBattle(unittest.TestCase):
    def setUp(self) -> None:
        player_team = Team("Player")
        enemy_team = Team("Enemy")
        self.battle = Battle(player_team, enemy_team)

        print("\n")

    def test_create_action(self):
        # Check triggered ability
        ability = {"trigger": TriggerEvent.TestTrigger, "effect": {"kind": EffectKind.test_effect}}
        pet = MagicMock(ability=ability)

        action = self.battle.create_action(pet, pet.ability, TriggerEvent.TestTrigger)
        self.assertEqual(action.__dict__, {"pet": pet, "method": EffectKind.test_effect, "kwargs": {}})

        # Check ability not triggered
        action = self.battle.create_action(pet, pet.ability, None)
        self.assertFalse(action)

    def test_enqueue(self):
        action = MagicMock()
        priority = 0

        self.battle.enqueue(priority, action)

        self.assertEqual(self.battle.action_queue.queue, [(0, 0.0, action)])

    @patch('src.pet_utils.pet.Pet.test_effect')
    def test_start_of_battle(self, mock_test_effect):
        # Prep 1 pet with trigger
        ability = {"trigger": TriggerEvent.StartOfBattle, "effect": {"kind": EffectKind.test_effect, "id": 0, "target": { "kind":EffectTargetKind.TestTarget, "n": 1}}}
        pet0 = Pet("0", ability_by_level={1: ability})
        pet1 = Pet("1")
        self.battle.player_team.pets_list = [pet0]
        self.battle.enemy_team.pets_list = [pet1]

        # Method
        self.battle.start_of_battle()

        # Check only 1 triggered
        self.assertEqual(mock_test_effect.call_count, 1)

    @patch('src.pet_utils.pet.Pet.test_effect')
    def test_before_attack(self, mock_test_effect):
        # Prep
        ability0 = {"trigger": TriggerEvent.BeforeAttack, "effect": {"kind": EffectKind.test_effect, "id": 0}}
        ability1 = {"trigger": TriggerEvent.BeforeAttack, "effect": {"kind": EffectKind.test_effect, "id": 1}}
        pet0 = Pet("", ability_by_level={1: ability0}, base_attack=1)
        pet1 = Pet("", ability_by_level={1: ability1}, base_attack=10)
        self.battle.player_team.pets_list = [pet0]
        self.battle.enemy_team.pets_list = [pet1]

        # Method
        self.battle.before_attack()

        # Ensure both pets triggered effect
        self.assertEqual(mock_test_effect.call_count, 2)

        # Ensure higher attack pet executed first
        first_call_args, first_call_kwargs = mock_test_effect.call_args_list[0]
        second_call_args, second_call_kwargs = mock_test_effect.call_args_list[1]

        self.assertEqual(first_call_kwargs["id"], 1)
        self.assertEqual(second_call_kwargs["id"], 0)

    @patch('src.pet_utils.pet.Pet.test_effect')
    def test_after_attack(self, mock_test_effect):
        # Prep for both pets surviving
        ability0 = {"trigger": TriggerEvent.AfterAttack, "effect": {"kind": EffectKind.test_effect, "id": 0}}
        ability1 = {"trigger": TriggerEvent.AfterAttack, "effect": {"kind": EffectKind.test_effect, "id": 1}}
        pet0 = Pet("", ability_by_level={1: ability0}, base_attack=1)
        pet1 = Pet("", ability_by_level={1: ability1}, base_attack=10)
        self.battle.player_team.add_pet(pet0)
        self.battle.enemy_team.add_pet(pet1)
        fighters = [pet for pet in self.battle.fighters if pet.alive]

        # Method
        self.battle.after_attack(fighters)

        # Test method called for both pets
        self.assertEqual(mock_test_effect.call_count, 2)

        # Test higher attack ability triggered first
        first_call_args, first_call_kwargs = mock_test_effect.call_args_list[0]
        second_call_args, second_call_kwargs = mock_test_effect.call_args_list[1]
        self.assertEqual(first_call_kwargs["id"], 1)
        self.assertEqual(second_call_kwargs["id"], 0)

        # Prep for only 1 pet surviving
        self.battle.action_queue.clear_queue()
        pet0.base_health = 0
        fighters = [pet for pet in self.battle.fighters if pet.alive]

        # Method
        self.battle.after_attack(fighters)

        # Test method called for only 1 pet
        self.assertEqual(mock_test_effect.call_count, 1+2)  # 1 new one, 2 from earlier

    @patch('src.pet_utils.pet.Pet.test_effect')
    def test_fight_loop(self, mock_test_effect):
        # Prep a Before and After attack ability
        ability0 = {"trigger": TriggerEvent.BeforeAttack, "effect": {"kind": EffectKind.test_effect, "id": 0}}
        ability1 = {"trigger": TriggerEvent.AfterAttack, "effect": {"kind": EffectKind.test_effect, "id": 1}}
        pet0 = Pet("", ability_by_level={1: ability0}, base_attack=1)
        pet1 = Pet("", ability_by_level={1: ability1}, base_attack=1, base_health=2)
        self.battle.player_team.add_pet(pet0)
        self.battle.enemy_team.add_pet(pet1)

        # Method
        self.battle.fight_loop()

        # Test that pet1 is only survivor
        self.assertEqual(pet0.health, 0)
        self.assertEqual(pet1.health, 1)

        # Test that both effects called
        self.assertEqual(mock_test_effect.call_count, 2)

        # Test effects happened in order
        first_call_args, first_call_kwargs = mock_test_effect.call_args_list[0]
        second_call_args, second_call_kwargs = mock_test_effect.call_args_list[1]
        self.assertEqual(first_call_kwargs["id"], 0)
        self.assertEqual(second_call_kwargs["id"], 1)

    def test_pet_sending_action_to_queue(self):
        pet = Pet("TestPet")
        pet.team = self.battle.player_team
        pet.ability["triggered_by"] = TriggerByKind.Self
        signal = Signal(TriggerEvent.TestTrigger, pet, pet)

        expected_pet = pet
        expected_method = EffectKind.test_effect
        expected_kwargs = {"target": EffectTargetKind.TestTarget, "n": 1}

        pet.read_signal(signal)
        queued_action = self.battle.action_queue.queue[0][2]

        self.assertEqual(queued_action.pet, expected_pet)
        self.assertEqual(queued_action.method, expected_method)
        self.assertEqual(queued_action.kwargs, expected_kwargs)

    def test_attack(self):
        pet0 = Pet("0")
        pet1 = Pet("1")
        self.battle.player_team.add_pet(pet0)
        self.battle.enemy_team.add_pet(pet1)

        self.battle._attack()

        self.assertEqual(pet0.health, 0)
        self.assertEqual(pet1.health, 0)
        self.assertFalse(pet0.alive)

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



