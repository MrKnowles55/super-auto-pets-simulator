import unittest
from tests.dummy.dummy_action import generate_dummy_action
from tests.dummy.dummy_pet import generate_dummy_pet
from tests.dummy.dummy_ability import generate_dummy_ability
from tests.dummy.dummy_team import Dummy_Team

from src.action.action_utils import ActionHandler
from src.pet_data_utils.enums.trigger_event import TriggerEvent


def modify_ability_apply(ability, action_name, action_source, action_trigger_event, **action_kwargs):
    def new_apply_method(*args, **kwargs):
        return [generate_dummy_action(action_name, action_source, action_trigger_event, **action_kwargs)]

    ability.apply = new_apply_method
    return ability


class TestActionHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.action_list = []
        self.priority_dict = {}
        self.team_action_list = []

        self.handler = ActionHandler()

    def test_add_action(self):
        action_name = "name"
        action_source = generate_dummy_pet()
        action_trigger_event = TriggerEvent.Test
        action_kwargs = {"foo": 1, "bar": 2}
        dummy_action = generate_dummy_action(action_name, action_source, action_trigger_event, **action_kwargs)
        action_list = [dummy_action, dummy_action]

        # Add single action
        self.handler.add_action(dummy_action)

        self.assertEqual(self.handler.action_list[0], dummy_action)
        self.assertEqual(len(self.handler.action_list), 1)

        # Add list of actions
        self.handler.add_action(action_list)

        self.assertEqual(len(self.handler.action_list), 3)

    def test_remove_actions(self):
        action_name = "name"
        action_source = generate_dummy_pet()
        action_trigger_event = TriggerEvent.Test
        action_kwargs = {"foo": 1, "bar": 2}
        dummy_action = generate_dummy_action(action_name, action_source, action_trigger_event, **action_kwargs)

        # Remove single action with list of len 1
        self.handler.action_list.append(dummy_action)
        self.handler.remove_actions(dummy_action)

        self.assertFalse(self.handler.action_list)

        # Remove single action with large list
        self.handler.action_list = []
        self.handler.action_list.append(dummy_action)
        self.handler.action_list.append(dummy_action)
        self.handler.remove_actions(dummy_action)

        self.assertEqual(len(self.handler.action_list), 1)

        # Remove list of actions
        self.handler.action_list = []
        self.handler.action_list.append(dummy_action)
        self.handler.action_list.append(dummy_action)
        self.handler.remove_actions([dummy_action, dummy_action])

        self.assertFalse(self.handler.action_list)

    def test_clear_actions(self):
        action_name = "name"
        action_source = generate_dummy_pet()
        action_trigger_event = TriggerEvent.Test
        action_kwargs = {"foo": 1, "bar": 2}
        test_action = generate_dummy_action(action_name, action_source, action_trigger_event, **action_kwargs)

        # Clear action list
        self.handler.action_list.append(test_action)
        self.handler.action_list.append(test_action)
        self.handler.action_list.append(test_action)

        self.handler.clear_actions()

        self.assertFalse(self.handler.action_list)

    def test_execute_actions(self):
        pass

    def test_execute(self):
        pass

    def test_execute_damage(self):
        dummy_pet = generate_dummy_pet()
        dummy_team = Dummy_Team()
        dummy_action = generate_dummy_action(name="Damage", source=dummy_pet, target_pet=dummy_pet, damage_amount=1)
        # 1 Damage
        self.handler._execute_damage(dummy_action)

        self.assertFalse(dummy_pet.is_alive)
        self.assertEqual(dummy_pet.health, 0)

    def test_execute_remove(self):
        dummy_pet = generate_dummy_pet()
        dummy_team = Dummy_Team()
        dummy_team.add_pet(dummy_pet)
        dummy_action = generate_dummy_action(name="Remove", source=dummy_team, team=dummy_team, pet_to_remove=dummy_pet)

        self.assertTrue(dummy_team.pets_list)

        self.handler._execute_remove(dummy_action)

        self.assertFalse(dummy_team.pets_list)

    def test_execute_summon(self):
        dummy_pet = generate_dummy_pet()
        dummy_team = Dummy_Team()
        dummy_action = generate_dummy_action(name="Summon", source=dummy_pet, team=dummy_team, pet_to_summon="sloth",
                                             index=0)

        # Add to front
        self.assertFalse(dummy_team.pets_list)

        self.handler._execute_summon(dummy_action)

        self.assertEqual(dummy_team.length, 1)
        self.assertEqual(dummy_team.pets_list[0].name, "Sloth")

        # Add with index
        dummy_action = generate_dummy_action(name="Summon", source=dummy_pet, team=dummy_team, pet_to_summon="sloth",
                                             index=1)
        dummy_team.pets_list = [dummy_pet, dummy_pet]

        self.handler._execute_summon(dummy_action)

        self.assertEqual(dummy_team.length, 3)
        self.assertEqual(dummy_team.pets_list[1].name, "Sloth")

    def test_execute_modify_stats(self):
        dummy_pet = generate_dummy_pet()
        dummy_target = generate_dummy_pet(name="target pet")
        dummy_team = Dummy_Team()
        dummy_team.add_pet(dummy_pet)

        base_action_dict = {
            'name': "Modify_Stats",
            'source': dummy_pet,
            'target_pet': dummy_target,
            'attack_mod': 1,
            'health_mod': 1,
            'transfer_to': False,
            'transfer_from': False,
            'percentage': None
        }
        dummy_action = generate_dummy_action(**base_action_dict)

        print()
        print(dummy_pet.display(), dummy_target.display())

        # +1/+1 from 1 pet to another pet

        self.handler._execute_modify_stats(dummy_action, retarget_flag=False)

        self.assertEqual(dummy_target.attack, 2)
        self.assertEqual(dummy_target.health, 2)

        # +1/+1 to pet that does not exist
        dummy_action = generate_dummy_action(**base_action_dict)
        dummy_action.kwargs["target_pet"] = None

        self.handler._execute_modify_stats(dummy_action, retarget_flag=False)

    def test_prioritize_actions(self):
        pet_small = generate_dummy_pet(attack=1)
        pet_large = generate_dummy_pet(attack=50)
        action_small = generate_dummy_action(source=pet_small)
        action_large = generate_dummy_action(source=pet_large)
        self.handler.action_list.append(action_small)
        self.handler.action_list.append(action_large)

        self.handler.prioritize_actions()

        self.assertEqual(self.handler.priority_dict[50], [action_large])
        self.assertEqual(self.handler.priority_dict[49.5], [])
        self.assertEqual(self.handler.priority_dict[1], [action_small])

    def test_retarget_action(self):
        dummy_pet = generate_dummy_pet()
        dummy_ability = generate_dummy_ability(owner=dummy_pet, trigger_event="Test")
        action_name = "name"
        action_source = dummy_pet
        action_trigger_event = TriggerEvent.Test
        action_kwargs = {"foo": 1, "bar": 2}
        dummy_ability = modify_ability_apply(dummy_ability, action_name, action_source, action_trigger_event,
                                             **action_kwargs)
        dummy_pet.ability = dummy_ability
        dummy_action = generate_dummy_action(action_name, action_source, action_trigger_event, **action_kwargs)

        result = self.handler.retarget_action(dummy_action)
        self.assertEqual(result.name, dummy_action.name)
        self.assertEqual(result.source, dummy_action.source)
        self.assertEqual(result.kwargs, dummy_action.kwargs)
