import unittest

from data.old.depreciated.pet_entity import PetEntity

from data.old.depreciated.dummy.dummy_ability import generate_dummy_ability
from data.old.depreciated.dummy.dummy_action import Dummy_ActionHandler
from data.old.depreciated.dummy.dummy_team import Dummy_Team


class FakeAbilityGenerator:
    def __init__(self, ability_dict, owner):
        self.ability_dict = ability_dict
        self.owner = owner

    def generate(self):
        return generate_dummy_ability(self.owner, trigger_event=None)


class TestPetEntity(unittest.TestCase):

    def setUp(self):
        self.action_handler = Dummy_ActionHandler()
        # Cleanup ActionHandler
        self.action_handler.clear_actions()

        # Setup default abilities for PetEntity Initialization
        self.test_ability_data = {}
        self.test_ability = generate_dummy_ability(None)
        self.test_ability_generator = FakeAbilityGenerator

        # Initialize 2 pets.

        self.pet = PetEntity("name", 1, 1, 1, 1, self.test_ability_data, self.test_ability_data, self.test_ability_data,
                             self.test_ability_generator, self.action_handler)

        self.enemy_pet = PetEntity("enemy", 1, 1, 1, 1, self.test_ability_data, self.test_ability_data,
                                   self.test_ability_data, self.test_ability_generator, self.action_handler)

    def test_pet_creation(self):
        # Check pet_utils initialization has expected results
        expected_name = "name"
        expected_attack = 1
        expected_health = 1
        expected_tier = 1
        expected_level = 1
        expected_ability_data = self.test_ability_data
        expected_ability = self.test_ability

        # Create a PetEntity with the expected values
        pet = PetEntity(expected_name, expected_attack, expected_health, expected_tier, expected_level,
                        expected_ability_data, expected_ability_data, expected_ability_data,
                        self.test_ability_generator, self.action_handler)

        # Assert that the PetEntity attributes are set correctly
        self.assertEqual(pet.name, expected_name)
        self.assertEqual(pet.attack, expected_attack)
        self.assertEqual(pet.health, expected_health)
        self.assertEqual(pet.tier, expected_tier)
        self.assertEqual(pet.level, expected_level)
        self.assertEqual(pet.ability_dicts[1], expected_ability_data)
        self.assertEqual(pet.ability_dicts[2], expected_ability_data)
        self.assertEqual(pet.ability_dicts[3], expected_ability_data)
        self.assertIsInstance(pet.abilities[1], type(expected_ability))
        self.assertIsInstance(pet.abilities[2], type(expected_ability))
        self.assertIsInstance(pet.abilities[3], type(expected_ability))
        self.assertEqual(pet.ability, pet.abilities[1])
        self.assertEqual(pet.team, None)
        self.assertEqual(pet.fainted, False)

    def test_pet_is_alive(self):
        self.pet.health = 1
        self.assertTrue(self.pet.is_alive)

        self.pet.health = 50
        self.assertTrue(self.pet.is_alive)

        self.pet.health = 0
        self.assertFalse(self.pet.is_alive)

        self.pet.health = -50
        self.assertFalse(self.pet.is_alive)

    def test_apply_damage(self):
        # Set pet_utils stats
        self.pet.attack = 1
        self.pet.health = 50

        # set enemy pet_utils stats
        self.enemy_pet.attack = 0
        self.enemy_pet.health = 50

        self.pet.apply_damage(self.enemy_pet.attack, self.enemy_pet)
        self.enemy_pet.apply_damage(self.pet.attack, self.pet)

        self.assertEqual(self.pet.health, 50)
        self.assertEqual(self.enemy_pet.health, 49)

    def test_hurt(self):
        # No action_utils returned when trigger_event is not Hurt
        self.pet.ability = generate_dummy_ability(self.pet)
        self.pet.hurt()
        self.assertEqual(self.action_handler.action_list, [])

        # Hurt action_utils returned when trigger_event is Hurt
        self.pet.ability = generate_dummy_ability(self.pet, "Hurt")
        self.pet.hurt()

        self.assertIn(self.action_handler.action_list[0][0], "Hurt")

    def test_faint(self):
        attacker = self.enemy_pet
        ability_none = generate_dummy_ability(self.pet)
        ability_faint = generate_dummy_ability(self.pet, "Faint")
        # No action_utils returned when trigger_event is not Faint
        self.action_handler.clear_actions()
        self.pet.fainted = False
        self.pet.ability = ability_none

        self.pet.faint(attacker)

        self.assertEqual(self.action_handler.action_list, [])
        self.assertTrue(self.pet.fainted)

        # Faint action_utils returned when trigger_event is Faint
        self.action_handler.clear_actions()
        self.pet.fainted = False
        self.pet.ability = ability_faint

        self.pet.faint(attacker)

        self.assertIn(self.action_handler.action_list[0][0], "Faint")
        self.assertTrue(self.pet.fainted)

        # Assure pet_utils cannot faint twice
        self.action_handler.clear_actions()
        self.pet.fainted = True
        self.pet.ability = ability_faint

        self.pet.faint(attacker)

        self.assertEqual(self.action_handler.action_list, [])
        self.assertTrue(self.pet.fainted)

        # Assure pet_utils is cleaned up if faint ability does not remove the pet_utils from team_utils
        self.action_handler.clear_actions()
        self.pet.fainted = False
        self.pet.ability = ability_none
        self.pet.health = 0
        team = Dummy_Team()
        team.add_pet(self.pet)
        self.pet.team = team

        self.pet.faint(attacker)

        self.assertFalse(team.pets_list)

    def test_before_attack(self):
        # No action_utils returned when trigger_event is not BeforeAttack
        self.pet.ability = generate_dummy_ability(self.pet)
        self.pet.before_attack()
        self.assertEqual(self.action_handler.action_list, [])

        # BeforeAttack action_utils returned when trigger_event is BeforeAttack
        self.pet.ability = generate_dummy_ability(self.pet, "BeforeAttack")
        self.pet.before_attack()

        self.assertIn(self.action_handler.action_list[0][0], "BeforeAttack")

    def test_attack_pet(self):
        # Set pet_utils stats
        self.pet.attack = 1
        self.pet.health = 50

        # set enemy pet_utils stats
        self.enemy_pet.attack = 0
        self.enemy_pet.health = 50
        self.pet.attack_pet(self.enemy_pet)

        self.assertEqual(self.pet.health, 50)
        self.assertEqual(self.enemy_pet.health, 49)


if __name__ == '__main__':
    unittest.main()
