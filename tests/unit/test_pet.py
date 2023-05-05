import unittest
from src.pet.pet_entity import PetEntity
from src.config_utils.logger import setup_logger, log_call, log_class_init
from src.action.action_utils import action_handler
from tests.unit.ability.test_ability import generate_test_ability
from src.team.team import Team
log = setup_logger(__name__)


@log_class_init(log)
class TestAbilityGenerator:
    def __init__(self, ability_dict, owner):
        self.ability_dict = ability_dict
        self.owner = owner

    def generate(self):
        return generate_test_ability(self.owner, trigger_event=None)


@log_class_init(log)
class TestPet(unittest.TestCase):

    @log_call(log)
    def setUp(self):
        # Cleanup ActionHandler
        action_handler.clear_actions()

        # Setup default abilities for PetEntity Initialization
        self.test_ability_data = {}
        self.test_ability = generate_test_ability(None)
        self.test_ability_generator = TestAbilityGenerator

        # Initialize 2 pets.

        self.pet = PetEntity("name", 1, 1, 1, 1, self.test_ability_data, self.test_ability_data, self.test_ability_data,
                             self.test_ability_generator)

        self.enemy_pet = PetEntity("enemy", 1, 1, 1, 1, self.test_ability_data, self.test_ability_data,
                                   self.test_ability_data, self.test_ability_generator)

    @log_call(log)
    def test_pet_creation(self):
        # Check pet initialization has expected results
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
                        self.test_ability_generator)

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
        # Set pet stats
        self.pet.attack = 1
        self.pet.health = 50

        # set enemy pet stats
        self.enemy_pet.attack = 0
        self.enemy_pet.health = 50

        self.pet.apply_damage(self.enemy_pet.attack, self.enemy_pet)
        self.enemy_pet.apply_damage(self.pet.attack, self.pet)

        self.assertEqual(self.pet.health, 50)
        self.assertEqual(self.enemy_pet.health, 49)

    def test_hurt(self):
        # No action returned when trigger_event is not Hurt
        self.pet.ability = generate_test_ability(self.pet)
        self.pet.hurt()
        self.assertEqual(action_handler.action_list, [])

        # Hurt action returned when trigger_event is Hurt
        self.pet.ability = generate_test_ability(self.pet, "Hurt")
        self.pet.hurt()

        self.assertIn(action_handler.action_list[0][0], "Hurt")

    def test_faint(self):
        attacker = self.enemy_pet
        ability_none = generate_test_ability(self.pet)
        ability_faint = generate_test_ability(self.pet, "Faint")
        # No action returned when trigger_event is not Faint
        action_handler.clear_actions()
        self.pet.fainted = False
        self.pet.ability = ability_none

        self.pet.faint(attacker)

        self.assertEqual(action_handler.action_list, [])
        self.assertTrue(self.pet.fainted)

        # Faint action returned when trigger_event is Faint
        action_handler.clear_actions()
        self.pet.fainted = False
        self.pet.ability = ability_faint

        self.pet.faint(attacker)

        self.assertIn(action_handler.action_list[0][0], "Faint")
        self.assertTrue(self.pet.fainted)

        # Assure pet cannot faint twice
        action_handler.clear_actions()
        self.pet.fainted = True
        self.pet.ability = ability_faint

        self.pet.faint(attacker)

        self.assertEqual(action_handler.action_list, [])
        self.assertTrue(self.pet.fainted)

        # Assure pet is cleaned up if faint ability does not remove the pet from team
        action_handler.clear_actions()
        self.pet.fainted = False
        self.pet.ability = ability_none
        self.pet.health = 0
        test_team = Team("Test")
        test_team.pets.append(self.pet)
        self.pet.team = test_team

        self.pet.faint(attacker)

        self.assertFalse(test_team.pets)

    def test_before_attack(self):
        # No action returned when trigger_event is not BeforeAttack
        self.pet.ability = generate_test_ability(self.pet)
        self.pet.before_attack()
        self.assertEqual(action_handler.action_list, [])

        # BeforeAttack action returned when trigger_event is BeforeAttack
        self.pet.ability = generate_test_ability(self.pet, "BeforeAttack")
        self.pet.before_attack()

        self.assertIn(action_handler.action_list[0][0], "BeforeAttack")

    def test_attack_pet(self):
        # Set pet stats
        self.pet.attack = 1
        self.pet.health = 50

        # set enemy pet stats
        self.enemy_pet.attack = 0
        self.enemy_pet.health = 50
        self.pet.attack_pet(self.enemy_pet)

        self.assertEqual(self.pet.health, 50)
        self.assertEqual(self.enemy_pet.health, 49)


if __name__ == '__main__':
    unittest.main()
