import unittest
from unittest.mock import MagicMock

from src.pet_utils.pet import Pet

from src.data_utils.enums.trigger_event import TriggerEvent
from src.data_utils.enums.trigger_by_kind import TriggerByKind
from src.data_utils.enums.effect_target_kind import EffectTargetKind
from src.data_utils.enums.effect_kind import EffectKind


class TestPet(unittest.TestCase):
    def setUp(self):
        self.pet = Pet("TestPet")
        # self.friend_pet = Pet("FriendPet")
        # self.enemy_pet = Pet("FriendPet")
        print("\n")

    def test_pet_init(self):
        """
        Test pet_utils creation and initialization
        :return:
        """
        expected_dict = {
            # Not checking id because the tests are run in random order, so no guarantee on what the id will be
            "name": "TestPet",
            "base_attack": 1,
            "base_health": 1,
            "tier": 1,
            "ability": {
                   "trigger": TriggerEvent.Test,
                   "triggered_by": TriggerByKind.Test,
                   "effect": EffectKind.Test,
                   "effect_dict": {"target": EffectTargetKind.Test}
               },
            "level": 1,
            "attack_mod": 0,
            "health_mod": 0,
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






