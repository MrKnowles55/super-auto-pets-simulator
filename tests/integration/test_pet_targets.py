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
        self.player_team = Team("Player")
        self.enemy_team = Team("Enemy")
        self.battle = Battle(self.player_team, self.enemy_team)

        print("\n")

    def test_target_adjacent_animals(self):
        pass

    def test_target_adjacent_friends(self):
        pass

    def test_target_all(self):
        pass

    def test_target_different_tier_animals(self):
        pass

    def test_target_each_enemy(self):
        pass

    def test_target_each_friend(self):
        pass

    def test_target_each_shop_animal(self):
        pass

    def test_target_first_enemy(self):
        pass

    def test_target_friend_ahead(self):
        pass

    def test_target_friend_behind(self):
        pass

    def test_target_highest_health_enemy(self):
        pass

    def test_target_last_enemy(self):
        pass

    def test_target_left_most_friend(self):
        pass

    def test_target_level2_and_3_friends(self):
        pass

    def test_target_lowest_health_enemy(self):
        pass

    def test_target_random_enemy(self):
        fill_team(self.player_team, 1)

        test_pet = self.player_team.first
        # Check Max targets selected

        # Enemy count from 1 to 5
        for e in range(1, 6):
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
        pass

    def test_target_right_most_friend(self):
        pass

    def test_target_self(self):
        pass

    def test_target_triggering_entity(self):
        pass

    def test_target_left_most_shop_animal(self):
        pass
