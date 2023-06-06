import unittest
from unittest.mock import MagicMock, patch

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
        print("\n\n")

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
            "ability_by_level": {1: {'description': 'Test level 1 Ability', 'trigger': TriggerEvent.TestTrigger,
                                     'triggered_by': TriggerByKind.TestTriggeredby,
                                     'effect': {'kind': EffectKind.test_effect, "target": EffectTargetKind.TestTarget}},
                                 2: {'description': 'Test level 2 Ability', 'trigger': TriggerEvent.TestTrigger,
                                     'triggered_by': TriggerByKind.TestTriggeredby,
                                     'effect': {'kind': EffectKind.test_effect, "target": EffectTargetKind.TestTarget}},
                                 3: {'description': 'Test level 3 Ability', 'trigger': TriggerEvent.TestTrigger,
                                     'triggered_by': TriggerByKind.TestTriggeredby,
                                     'effect': {'kind': EffectKind.test_effect,
                                                "target": EffectTargetKind.TestTarget}}},

            "level": 1,
            "attack_mod": 0,
            "health_mod": 0,
            "team": None,
            "start_position": -1,
            "position": -1
        }

        for key, value in expected_dict.items():
            self.assertEqual(self.pet.__dict__[key], value)

        # Properties
        self.assertEqual(self.pet.attack, 1)
        self.assertEqual(self.pet.health, 1)
        self.assertEqual(self.pet.ability, {'description': 'Test level 1 Ability', 'trigger': TriggerEvent.TestTrigger,
                                            'triggered_by': TriggerByKind.TestTriggeredby,
                                            'effect': {'kind': EffectKind.test_effect,
                                                       "target": EffectTargetKind.TestTarget}})
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
            "ability_by_level": {
                1: {
                    'description': 'Overwritten 1',
                    'trigger': TriggerEvent.TestTrigger,
                    'triggered_by': TriggerByKind.TestTriggeredby,
                    'effect': {
                        'kind': EffectKind.test_effect,
                        "target": {
                                "kind": EffectTargetKind.TestTarget
                                  }
                              }
                    },
                2: {
                    'description': 'Overwritten 2',
                    'trigger': TriggerEvent.TestTrigger,
                    'triggered_by': TriggerByKind.TestTriggeredby,
                    'effect': {
                        'kind': EffectKind.test_effect,
                        "target": {
                                "kind": EffectTargetKind.TestTarget
                                  }
                              }
                    },
                3: {'description': 'Overwritten 3',
                    'trigger': TriggerEvent.TestTrigger,
                    'triggered_by': TriggerByKind.TestTriggeredby,
                    'effect': {
                        'kind': EffectKind.test_effect,
                        "target": {
                            "kind": EffectTargetKind.TestTarget
                                  }
                              }
                    }
            },

            "level": 2,
            "attack_mod": 9,
            "health_mod": 8,
            "team": None,
            "start_position": -1,
            "position": -1
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

        # Properties
        self.assertEqual(cool_pet.attack, 20)
        self.assertEqual(cool_pet.health, 30)
        self.assertEqual(cool_pet.level, 2)
        self.assertEqual(cool_pet.ability, {'description': 'Overwritten 2', 'trigger': TriggerEvent.TestTrigger,
                                            'triggered_by': TriggerByKind.TestTriggeredby,
                                            'effect': {'kind': EffectKind.test_effect,
                                                       "target": {"kind": EffectTargetKind.TestTarget}}})

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

    def test_read_signal(self):
        """
        Pet sends a fake signal to itself, ensuring that it is triggered by it and reads the signal.
        The signal is then sent to its fake team, and fake action handler, to be put into the fake queue.
        :return:
        """
        # Fake signal
        signal = MagicMock()
        signal.message = TriggerEvent.TestTrigger
        signal.sender = self.pet
        signal.receiver = self.pet

        # Ensure pet will be triggered by self
        self.pet.ability["triggered_by"] = TriggerByKind.Self

        # Fake action handler and queue
        battle = MagicMock()
        battle.action_queue = []

        # Fake action to add to queue
        action = MagicMock()
        action.pet = self.pet
        action.method = self.pet.test_effect
        action.kwargs = None

        # Fake team to create and send action
        team = MagicMock()
        team.create_action.return_value = action
        team.send_action.side_effect = battle.action_queue.append(action)
        self.pet.team = team

        # Execute
        self.pet.read_signal(signal)

        # Check that action was sent, and queue updated
        self.assertEqual(team.send_action.call_count, 1)
        team.send_action.assert_called_with(action)
        self.assertEqual(battle.action_queue, [action])

    def test_attack_pet(self):
        enemy = Pet("Enemy")
        self.pet.attack_pet(enemy)

        self.assertEqual(enemy.health, 0)
        self.assertFalse(enemy.alive)

    def test_update(self):
        team = MagicMock()
        team.pets_list = [self.pet]
        self.pet.team = team

        def remove_pet_side_effect(pet):
            if not pet.alive:
                team.pets_list.pop(pet.position)

        team.remove_pet.side_effect = remove_pet_side_effect

        # Update with living pet
        self.pet.update()

        self.assertEqual(team.pets_list, [self.pet])

        # Update with dead pet
        self.pet.damage = self.pet.base_health + self.pet.health_mod

        self.pet.update()

        self.assertEqual(team.pets_list, [])
