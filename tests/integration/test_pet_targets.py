import logging
import unittest
from unittest.mock import MagicMock, patch

from src.pet_utils.pet import Pet
from src.action_utils.battle import Battle, Action, PriorityQueue
from src.team_utils.team import Team
from src.action_utils.signals import send_signal, Signal
from src.config_utils.custom_logger import setup_logging
from src.data_utils.ability_enums import EffectKind, EffectTargetKind, TriggerByKind, TriggerEvent

setup_logging(logging.DEBUG)


def fill_team(team, size):
    team.pets_list = []
    for _ in range(size):
        team.add_pet(Pet(f"{team.name[0]}"))


class TestPet_Target(unittest.TestCase):
    def setUp(self) -> None:
        setup_logging(logging.DEBUG)
        self.player_team = Team("Player")
        self.enemy_team = Team("Enemy")
        self.battle = Battle(self.player_team, self.enemy_team)

        print("\n")

    def test_target_adjacent_animals(self):
        # Test full teams and n from 1 to 3
        fill_team(self.player_team, 5)
        fill_team(self.enemy_team, 5)

        test_pet = self.player_team.first
        for n in range(1, 4):

            targets = test_pet.target_adjacent_animals(n=n)
            self.assertEqual(len(targets), n*2)
            self.assertEqual(targets[0], self.player_team.pets_list[n])
            self.assertEqual(targets[-1], self.enemy_team.pets_list[n-1])

        # Test incomplete target
        fill_team(self.player_team, 3)
        fill_team(self.enemy_team, 1)

        test_pet = self.player_team.first
        targets = test_pet.target_adjacent_animals(n=2)
        self.assertEqual(len(targets), 3)
        print(self.player_team.pets_list, targets)
        self.assertEqual(self.player_team.pets_list[1], targets[1])

    def test_target_adjacent_friends(self):
        # Test full team and n from 1 to 3
        fill_team(self.player_team, 5)

        # Loop over each pet
        for test_pet in self.player_team.pets_list:

            # Loop over n from 1 to 3
            for n in range(1, 4):
                targets = test_pet.target_adjacent_friends(n=n)
                print(targets)

    def test_target_all(self):
        fill_team(self.player_team, 5)
        fill_team(self.enemy_team, 5)

        test_pet = self.player_team.first
        targets = test_pet.target_all()

        # May need to remove self from targets
        self.assertEqual(len(targets), 10)
        # self.assertNotIn(test_pet, targets)

    def test_target_different_tier_animals(self):
        # All different tiers
        fill_team(self.player_team, 5)
        for i, pet in enumerate(self.player_team.pets_list):
            pet.tier = i
        test_pet = self.player_team.first
        targets = test_pet.target_different_tier_animals()
        self.assertEqual(len(targets), 4)
        self.assertNotIn(test_pet, targets)

        # All same tier
        for pet in self.player_team.pets_list:
            pet.tier = 1
        targets = test_pet.target_different_tier_animals()
        self.assertEqual(len(targets), 1)

    def test_target_each_enemy(self):
        fill_team(self.player_team, 5)
        fill_team(self.enemy_team, 5)

        test_pet = self.player_team.first
        targets = test_pet.target_each_enemy()

        # May need to remove self from targets
        self.assertEqual(len(targets), 5)

    def test_target_each_friend(self):
        fill_team(self.player_team, 5)

        test_pet = self.player_team.first
        targets = test_pet.target_each_friend()

        # May need to remove self from targets
        self.assertEqual(len(targets), 4)

    def test_target_each_shop_animal(self):
        pass

    def test_target_first_enemy(self):
        fill_team(self.player_team, 1)
        fill_team(self.enemy_team, 5)

        test_pet = self.player_team.first
        targets = test_pet.target_first_enemy()

        # May need to remove self from targets
        self.assertEqual([self.enemy_team.first], targets)

    def test_target_friend_ahead(self):
        fill_team(self.player_team, 5)
        # Loop over each pet, then for n from 1 to 3
        for test_pet in self.player_team.pets_list:
            for n in range(1, 4):
                targets = test_pet.target_friend_ahead(n=n)
                self.assertEqual(len(targets), min(n, test_pet.position))
                if targets:
                    index = test_pet.position
                    self.assertIn(self.player_team.pets_list[index-1], targets)

    def test_target_friend_behind(self):
        fill_team(self.player_team, 5)
        # Loop over each pet, then for n from 1 to 3
        for test_pet in self.player_team.pets_list:
            for n in range(1, 4):
                targets = test_pet.target_friend_behind(n=n)
                self.assertEqual(len(targets), min(n, 5 - test_pet.position - 1))
                if targets:
                    index = test_pet.position
                    self.assertIn(self.player_team.pets_list[index + 1], targets)

    def test_target_highest_health_enemy(self):
        fill_team(self.player_team, 1)
        fill_team(self.enemy_team, 5)
        for pet in self.enemy_team.pets_list:
            pet.base_health += pet.position

        test_pet = self.player_team.first
        targets = test_pet.target_highest_health_enemy()
        self.assertEqual([self.enemy_team.pets_list[-1]], targets)

    def test_target_last_enemy(self):
        fill_team(self.player_team, 1)
        fill_team(self.enemy_team, 5)

        test_pet = self.player_team.first
        targets = test_pet.target_last_enemy()

        # May need to remove self from targets
        self.assertEqual([self.enemy_team.pets_list[-1]], targets)


    def test_target_level2_and_3_friends(self):
        # All different levels
        fill_team(self.player_team, 4)
        for i in range(1, 4):
            self.player_team.pets_list[i].level = i
        test_pet = self.player_team.first
        targets = test_pet.target_level2_and_3_friends(n=3)
        self.assertEqual(len(targets), 2)
        self.assertIn(self.player_team.pets_list[2], targets)
        self.assertIn(self.player_team.pets_list[3], targets)

        # All same level
        for pet in self.player_team.pets_list:
            pet.level = 2
        targets = test_pet.target_level2_and_3_friends(n=3)
        self.assertEqual(len(targets), 3)

    def test_target_lowest_health_enemy(self):
        fill_team(self.player_team, 1)
        fill_team(self.enemy_team, 5)
        for pet in self.enemy_team.pets_list:
            pet.base_health += pet.position

        test_pet = self.player_team.first
        targets = test_pet.target_lowest_health_enemy()
        self.assertEqual([self.enemy_team.pets_list[0]], targets)

    def test_target_random_enemy(self):
        fill_team(self.player_team, 1)

        test_pet = self.player_team.first
        # Check Max targets selected

        # Enemy count from 0 to 5
        for e in range(0, 6):
            fill_team(self.enemy_team, e)

            # Target n from 1 to 5
            for n in range(1, 6):
                possible_targets = test_pet.team.other_team.pets_list
                targets = test_pet.target_random_enemy(n=n)

                # Ensure maximum number of targets selected
                self.assertEqual(len(targets), min(n, len(possible_targets)))

        # Check each pet can be selected
        self.assertEqual(self.enemy_team.length, 5)

        loop_counter = 0
        targeted_pets = set()
        # Coupon Collectors problem (average of 11 picks required to get all 5 selected at least once, 20 for safety)
        while len(targeted_pets) < 5 and loop_counter <= 20:
            targeted_pets.add(test_pet.target_random_enemy(n=1)[0])
            loop_counter += 1
        self.assertEqual(len(targeted_pets), 5)
        self.assertLess(loop_counter, 20)

    def test_target_random_friend(self):
        # Enemy count from 0 to 5
        for i in range(1, 6):
            fill_team(self.player_team, i)
            test_pet = self.player_team.first

            # Target n from 1 to 5
            for n in range(1, 5):
                possible_targets = [pet for pet in self.player_team.pets_list if pet != test_pet]
                targets = test_pet.target_random_friend(n=n)

                # Ensure maximum number of targets selected
                self.assertEqual(len(targets), min(n, len(possible_targets)))

        # Check each pet can be selected
        test_pet = self.player_team.first
        loop_counter = 0
        targeted_pets = set()
        # Coupon Collectors problem (average of 11 picks required to get all 5 selected at least once, 20 for safety)
        while len(targeted_pets) < 4 and loop_counter <= 20:
            targeted_pets.add(test_pet.target_random_friend(n=1)[0])
            loop_counter += 1
        self.assertEqual(len(targeted_pets), 4)
        self.assertLess(loop_counter, 20)

    def test_target_right_most_friend(self):
        fill_team(self.player_team, 5)
        for pet in self.player_team.pets_list:
            targets = pet.target_right_most_friend()
            # May need to remove self from targets
            self.assertEqual([self.player_team.first], targets)

    def test_target_self(self):
        pass

    def test_target_triggering_entity(self):
        pass

    def test_target_left_most_shop_animal(self):
        pass
