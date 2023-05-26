import unittest
from unittest.mock import MagicMock

from src.pet_utils.pet import Pet

from src.data_utils.enums.trigger_event import TriggerEvent
from src.data_utils.enums.trigger_by_kind import TriggerByKind
from src.data_utils.enums.effect_target_kind import EffectTargetKind
from src.data_utils.enums.effect_kind import EffectKind


class TestPet(unittest.TestCase):
    def setUp(self):
        self.pet = Pet("Test Pet")
        # self.friend_pet = Pet("FriendPet")
        # self.enemy_pet = Pet("FriendPet")
        print("\n")

    def test_pet_default(self):
        """
        Test pet_utils creation and initialization
        :return:
        """
        expected_dict = {
            # Not checking id because the tests are run in random order, so no guarantee on what the id will be
            "name": "Test Pet",
            "base_attack": 1,
            "base_health": 1,
            "tier": -1,
            "ability_by_level": {1: {'description': 'Test level 1 Ability', 'trigger': TriggerEvent.Test, 'triggered_by': TriggerByKind.Test,
                                     'effect': {'kind': EffectKind.Test, "target": EffectTargetKind.Test}},
                                 2: {'description': 'Test level 2 Ability', 'trigger': TriggerEvent.Test, 'triggered_by': TriggerByKind.Test,
                                     'effect': {'kind': EffectKind.Test, "target": EffectTargetKind.Test}},
                                 3: {'description': 'Test level 3 Ability', 'trigger': TriggerEvent.Test, 'triggered_by': TriggerByKind.Test,
                                     'effect': {'kind': EffectKind.Test, "target": EffectTargetKind.Test}}},

            "level": 1,
            "attack_mod": 0,
            "health_mod": 0,
            "ability": {'description': 'Test level 1 Ability', 'trigger': TriggerEvent.Test, 'triggered_by': TriggerByKind.Test,
                        'effect': {'kind': EffectKind.Test, "target": EffectTargetKind.Test}},
            "team": None,
            "start_position": -1,
            "position": -1,
            "attack": 1,
            "health": 1
        }

        for key, value in expected_dict.items():
            self.assertEqual(self.pet.__dict__[key], value)

        # Properties
        self.assertTrue(self.pet.alive)
        self.assertEqual(self.pet.trigger, self.pet.ability.get("trigger"))
        self.assertEqual(self.pet.triggered_by, self.pet.ability.get("triggered_by"))

    def test_pet_init_override(self):
        expected_dict = {
            # Not checking id because the tests are run in random order, so no guarantee on what the id will be
            "name": "Test Pet",
            "base_attack": 11,
            "base_health": 22,
            "tier": 3,
            "ability_by_level": {1: {'description': 'Overwritten 1', 'trigger': TriggerEvent.Test, 'triggered_by': TriggerByKind.Test,
                                     'effect': {'kind': EffectKind.Test, "target": EffectTargetKind.Test}},
                                 2: {'description': 'Overwritten 2', 'trigger': TriggerEvent.Test, 'triggered_by': TriggerByKind.Test,
                                     'effect': {'kind': EffectKind.Test, "target": EffectTargetKind.Test}},
                                 3: {'description': 'Overwritten 3', 'trigger': TriggerEvent.Test, 'triggered_by': TriggerByKind.Test,
                                     'effect': {'kind': EffectKind.Test, "target": EffectTargetKind.Test}}},

            "level": 2,
            "attack_mod": 9,
            "health_mod": 8,
            "ability": {'description': 'Overwritten 2', 'trigger': TriggerEvent.Test, 'triggered_by': TriggerByKind.Test,
                        'effect': {'kind': EffectKind.Test, "target": EffectTargetKind.Test}},
            "team": None,
            "start_position": -1,
            "position": -1,
            "attack": 20,
            "health": 30
        }

        cool_pet = Pet(expected_dict["name"],
                       base_attack=expected_dict["base_attack"],
                       base_health=expected_dict["base_health"],
                       tier=expected_dict["tier"],
                       ability_by_level=expected_dict["ability_by_level"],
                       level=expected_dict["level"],
                       attack_mod=expected_dict["attack_mod"],
                       health_mod=expected_dict["health_mod"],
                       )
        for key, value in expected_dict.items():
            self.assertEqual(cool_pet.__dict__[key], value)

    def test_get_relationship(self):
        self.pet.team = MagicMock()
        self.pet.team.pets_list = [self.pet]

        # Self
        self.assertEqual(TriggerByKind.Self, self.pet.get_relationship(self.pet))

        # Enemy
        enemy_pet = Pet("EnemyPet")
        enemy_pet.team = MagicMock()
        enemy_pet.team.pets_list = [enemy_pet]

        self.assertEqual(TriggerByKind.EachEnemy, self.pet.get_relationship(enemy_pet))
        self.assertEqual(TriggerByKind.EachEnemy, enemy_pet.get_relationship(self.pet))

        # EachFriend & FriendAhead
        friend_pet = Pet("FriendPet")
        friend_pet.team = self.pet.team
        friend_pet.team.pets_list.append(friend_pet)

        # Friend behind test pet_utils should see FriendAhead, and test pet_utils sees EachFriend
        self.pet.position = 0
        friend_pet.position = 1

        self.assertEqual(TriggerByKind.EachFriend, self.pet.get_relationship(friend_pet))
        self.assertEqual(TriggerByKind.FriendAhead, friend_pet.get_relationship(self.pet))

        # Now the opposite
        self.pet.position = 1
        friend_pet.position = 0

        self.assertEqual(TriggerByKind.FriendAhead, self.pet.get_relationship(friend_pet))
        self.assertEqual(TriggerByKind.EachFriend, friend_pet.get_relationship(self.pet))

        # Player
        self.assertEqual(TriggerByKind.Player, self.pet.get_relationship(MagicMock()))
