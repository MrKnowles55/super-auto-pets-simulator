import unittest

from data.old.depreciated.dummy.dummy_pet import generate_big_pet

from src.pet_utils.pet_factory import create_pet
from data.old.depreciated.battle import fight
from data.old.depreciated.team import Team
from data.old.depreciated.action_utils import action_handler
from src.config_utils.logger import setup_logger, log_call, log_class_init

log = setup_logger(__name__)


@log_class_init(log)
class TestFlamingo(unittest.TestCase):

    @log_call(log)
    def setUp(self) -> None:
        self.handler = action_handler
        self.handler.clear_actions()

    def testSingle(self):
        team_a = Team("A")
        first_flamingo = create_pet("flamingo")
        team_a.add_pet(first_flamingo)

        team_b = Team("B")
        first_big = generate_big_pet()
        team_b.add_pet(first_big)

        # Check setup, 1 Flamingo vs 1 Big 50/50 pet_utils
        self.assertEqual(team_a.first, first_flamingo)
        self.assertEqual(team_b.first, first_big)

        # Fight
        fight(team_a, team_b)

        # Flamingo is dead, and Big dummy is alive
        self.assertFalse(team_a.pets_list)
        self.assertTrue(team_b.pets_list)

        # Big Dummy is hurt
        self.assertEqual(first_big.health, 50 - first_flamingo.attack)

    def testDouble(self):
        team_a = Team("A")
        first_flamingo = create_pet("flamingo")
        second_flamingo = create_pet("flamingo")
        team_a.add_pet(first_flamingo)
        team_a.add_pet(second_flamingo)

        team_b = Team("B")
        first_big = generate_big_pet()
        team_b.add_pet(first_big)

        # Test variables
        expected_damage = first_flamingo.attack + second_flamingo.attack + 1

        # Check setup, 1 Flamingo vs 1 Big 50/50 pet_utils
        self.assertEqual(team_a.pets_list, [first_flamingo, second_flamingo])
        self.assertEqual(team_b.first, first_big)

        # Fight
        fight(team_a, team_b)

        # Flamingos are dead, and Big dummy is alive
        self.assertFalse(team_a.pets_list)
        self.assertTrue(team_b.pets_list)

        # Damage equals Both flamingos attacks plus any modifiers
        self.assertEqual(first_big.health, 50 - expected_damage)
        self.assertEqual(expected_damage, first_flamingo.attack + second_flamingo.attack)

    def testTriple(self):
        team_a = Team("A")
        first_flamingo = create_pet("flamingo")
        second_flamingo = create_pet("flamingo")
        third_flamingo = create_pet("flamingo")
        team_a.add_pet(first_flamingo)
        team_a.add_pet(second_flamingo)
        team_a.add_pet(third_flamingo)

        team_b = Team("B")
        first_big = generate_big_pet()
        team_b.add_pet(first_big)

        # Test variables
        expected_damage = first_flamingo.attack + second_flamingo.attack + 1 + third_flamingo.attack + 2

        # Check setup, 1 Flamingo vs 1 Big 50/50 pet_utils
        self.assertEqual(team_a.pets_list, [first_flamingo, second_flamingo, third_flamingo])
        self.assertEqual(team_b.first, first_big)

        # Fight
        fight(team_a, team_b)

        # Flamingos are dead, and Big dummy is alive
        self.assertFalse(team_a.pets_list)
        self.assertTrue(team_b.pets_list)

        # Damage equals Both flamingos attacks plus any modifiers
        self.assertEqual(first_big.health, 50 - expected_damage)
        self.assertEqual(expected_damage, first_flamingo.attack + second_flamingo.attack + third_flamingo.attack)

    def testQuad(self):
        team_a = Team("A")
        first_flamingo = create_pet("flamingo")
        second_flamingo = create_pet("flamingo")
        third_flamingo = create_pet("flamingo")
        fourth_flamingo = create_pet("flamingo")
        team_a.add_pet(first_flamingo)
        team_a.add_pet(second_flamingo)
        team_a.add_pet(third_flamingo)
        team_a.add_pet(fourth_flamingo)

        team_b = Team("B")
        first_big = generate_big_pet()
        team_b.add_pet(first_big)

        # Test variables
        expected_damage = first_flamingo.attack + \
                          second_flamingo.attack + 1 + \
                          third_flamingo.attack + 2 + \
                          fourth_flamingo.attack + 2

        # Check setup, 1 Flamingo vs 1 Big 50/50 pet_utils
        self.assertEqual(team_a.pets_list, [first_flamingo, second_flamingo, third_flamingo, fourth_flamingo])
        self.assertEqual(team_b.first, first_big)

        # Fight
        fight(team_a, team_b)

        # Flamingos are dead, and Big dummy is alive
        self.assertFalse(team_a.pets_list)
        self.assertTrue(team_b.pets_list)

        # Damage equals Both flamingos attacks plus any modifiers
        self.assertEqual(first_big.health, 50 - expected_damage)
        self.assertEqual(expected_damage, first_flamingo.attack + second_flamingo.attack + third_flamingo.attack +
                         fourth_flamingo.attack)
