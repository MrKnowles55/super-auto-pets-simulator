import unittest
import data.old.depreciated.battle as battle
from data.old.depreciated.dummy.dummy_team import Dummy_Team
from data.old.depreciated.dummy.dummy_pet import generate_dummy_pet


class TestBattle(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_battle_string(self):
        pass
        # team1 = Dummy_Team("Team 1")
        # team2 = Dummy_Team("Team 2")
        # prefix = "Test prefix"
        # expected_value = "Test prefix                       pet_utils 4(1/1), pet_utils 3(1/1), pet_utils 2(1/1), pet_utils 1(1/1), " \
        #                  "pet_utils 0(1/1)     VS     pet_utils 0(1/1), pet_utils 1(1/1), pet_utils 2(1/1), pet_utils 3(1/1), pet_utils 4(1/1)" \
        #                  "                      "
        # name_length = 5
        # for _ in range(5):
        #     team1.add_pet(generate_dummy_pet("pet_utils "+str(_)+"excess text"))
        #     team2.add_pet(generate_dummy_pet("pet_utils "+str(_)+"excess text"))
        # self.assertEqual(battle.get_battle_string(team1, team2, prefix=prefix, name_length=name_length), expected_value)

    def test_get_pet_list(self):
        team1 = Dummy_Team("Team 1")
        team2 = Dummy_Team("Team 2")

        for _ in range(5):
            team1.add_pet(generate_dummy_pet("friendly "+str(_)))
            team2.add_pet(generate_dummy_pet("enemy "+str(_)))

        pet_list = battle.get_pet_list(team1, team2)

        for team in [team1, team2]:
            for pet in team.pets_list:
                self.assertIn(pet, pet_list)

    def test_start_of_battle(self):
        team1 = Dummy_Team("Team 1")
        team2 = Dummy_Team("Team 2")

        team1.add_pet(generate_dummy_pet("friendly"))
        team2.add_pet(generate_dummy_pet("enemy"))

        battle.start_of_battle(team1, team2)

    def test_perform_round(self):
        team1 = Dummy_Team("Team 1")
        team2 = Dummy_Team("Team 2")

        team1.add_pet(generate_dummy_pet("friendly"))
        team2.add_pet(generate_dummy_pet("enemy"))

        battle.perform_round(team1, team2)

    def test_before_attack(self):
        team1 = Dummy_Team("Team 1")
        team2 = Dummy_Team("Team 2")

        team1.add_pet(generate_dummy_pet("friendly"))
        team2.add_pet(generate_dummy_pet("enemy"))

        battle.before_attack(team1.first, team2.first)

    def test_attack(self):
        team1 = Dummy_Team("Team 1")
        team2 = Dummy_Team("Team 2")

        team1.add_pet(generate_dummy_pet("friendly"))
        team2.add_pet(generate_dummy_pet("enemy"))

        battle.attack(team1.first, team2.first)

    def test_after_attack(self):
        team1 = Dummy_Team("Team 1")
        team2 = Dummy_Team("Team 2")

        team1.add_pet(generate_dummy_pet("friendly"))
        team2.add_pet(generate_dummy_pet("enemy"))

        battle.after_attack(team1.first, team2.first)

    def test_is_battle_over(self):
        team1 = Dummy_Team("Team 1")
        team2 = Dummy_Team("Team 2")

        # Both empty
        self.assertTrue(battle.is_battle_over(team1, team2))

        # Team1 has pet_utils
        team1.add_pet(generate_dummy_pet("friendly"))

        self.assertTrue(battle.is_battle_over(team1, team2))

        # Both has pet_utils
        team2.add_pet(generate_dummy_pet("enemy"))

        self.assertFalse(battle.is_battle_over(team1, team2))

        # Team2 has pet_utils
        team1.pets_list = []

        self.assertTrue(battle.is_battle_over(team1, team2))

    def test_fight_loop(self):
        team1 = Dummy_Team("Team 1")
        team2 = Dummy_Team("Team 2")

        team1.add_pet(generate_dummy_pet("friendly"))
        team2.add_pet(generate_dummy_pet("enemy"))

        self.assertEqual(battle.fight_loop(team1, team2, loop_limit=10), 10)

    def test_end_of_battle(self):
        team1 = Dummy_Team("Team 1")
        team2 = Dummy_Team("Team 2")

        # Impossible Tie with both teams having a pet_utils

        team1.pets_list = []
        team2.pets_list = []

        for _ in range(5):
            team1.add_pet(generate_dummy_pet("friendly "+str(_)))
            team2.add_pet(generate_dummy_pet("enemy "+str(_)))

        self.assertEqual(battle.end_of_battle(team1, team2), [1, 1])

        # First team_utils wins

        team1.pets_list = []
        team2.pets_list = []

        for _ in range(5):
            team1.add_pet(generate_dummy_pet("friendly " + str(_)))

        self.assertEqual(battle.end_of_battle(team1, team2), [1, 0])

        # Second team_utils wins

        team1.pets_list = []
        team2.pets_list = []

        for _ in range(5):
            team2.add_pet(generate_dummy_pet("enemy " + str(_)))

        self.assertEqual(battle.end_of_battle(team1, team2), [0, 1])

        # Normal Tie

        team1.pets_list = []
        team2.pets_list = []

        self.assertEqual(battle.end_of_battle(team1, team2), [0, 0])

    def test_fight(self):
        pass

    def test_prioritize_pets(self):
        pet_list = []

        for _ in range(10):
            pet_list.append(generate_dummy_pet(attack=_, health=10-_))

        # Prioritize from the highest attack to lowest (Default)
        prioritized_pets = battle.prioritize_pets(pet_list)

        for priority, pets_with_priority in prioritized_pets.items():
            for pet in pets_with_priority:
                self.assertEqual(priority, pet.attack)

        # Prioritize from the highest health to lowest
        prioritized_pets = battle.prioritize_pets(pet_list, priority_key=lambda x: x.health)

        for priority, pets_with_priority in prioritized_pets.items():
            for pet in pets_with_priority:
                self.assertEqual(priority, pet.health)


if __name__ == '__main__':
    unittest.main()
