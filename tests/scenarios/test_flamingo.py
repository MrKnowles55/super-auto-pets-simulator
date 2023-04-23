import unittest
from pet_factory import create_pet
from battle import fight
from src.team.team import Team, opponent_team


class TestFlamingo(unittest.TestCase):

    def setUp(self) -> None:

        self.team_of_5 = Team("5 Flamingos")
        self.team_of_2 = Team("2 Flamingos")

        self.team_of_5.pets = [
            create_pet("Flamingo"),
            create_pet("Flamingo"),
            create_pet("Flamingo"),
            create_pet("Flamingo"),
            create_pet("Flamingo")
        ]

        self.team_of_2.pets = [
            create_pet("Flamingo"),
            create_pet("Flamingo")
        ]

        opponent_team.pets = [
            create_pet("Big Test"),
            create_pet("Big Test"),
            create_pet("Big Test"),
            create_pet("Big Test"),
            create_pet("Big Test")
        ]

        for pet in self.team_of_5.pets:
            pet.team = self.team_of_5
        for pet in self.team_of_2.pets:
            pet.team = self.team_of_2
        for pet in opponent_team.pets:
            pet.team = opponent_team

        self.teams_to_test = [self.team_of_5, self.team_of_2, opponent_team]

        # Store the initial pets for each team
        self.initial_pets = {
            self.team_of_5.name: self.team_of_5.pets[:],
            self.team_of_2.name: self.team_of_2.pets[:],
            opponent_team.name: opponent_team.pets[:]
        }

    def test_team_setup(self):

        # Check team sizes
        self.assertEqual(len(self.team_of_5.pets), 5)
        self.assertEqual(len(self.team_of_2.pets), 2)
        self.assertEqual(len(opponent_team.pets), 5)

        # Check teams have correct pets
        team_to_pet_dict = {
            self.team_of_5: ["Flamingo", 3],  # name and attack
            self.team_of_2: ["Flamingo", 3],
            opponent_team: ["Big Test", 50]
        }
        for team in self.teams_to_test:
            for pet in team.pets:
                self.assertEqual(pet.name, team_to_pet_dict[team][0])
                self.assertEqual(pet.attack, team_to_pet_dict[team][1])

    def test_flamingo_ability(self):

        # Knockout first Flamingo
        attacker = opponent_team.pets[0]
        self.team_of_5.pets[0].apply_damage(50, attacker)

        # check that Flamingo fainted
        self.assertEqual(len(self.team_of_5.pets), 4)

        # Check that the first 2 Flamingos behind the fainted one gain +1/+1
        self.assertEqual(self.team_of_5.pets[0].attack, 4)
        self.assertEqual(self.team_of_5.pets[0].health, 2)
        self.assertEqual(self.team_of_5.pets[1].attack, 4)
        self.assertEqual(self.team_of_5.pets[1].health, 2)

        # Check that last 2 Flamingos did not have stats modified
        self.assertEqual(self.team_of_5.pets[2].attack, 3)
        self.assertEqual(self.team_of_5.pets[2].health, 1)
        self.assertEqual(self.team_of_5.pets[3].attack, 3)
        self.assertEqual(self.team_of_5.pets[3].health, 1)

        # Check that Flamingo ability works when only 1 Target available
        self.team_of_2.pets[0].apply_damage(50, attacker)

        self.assertEqual(len(self.team_of_2.pets), 1)

        self.assertEqual(self.team_of_2.pets[0].attack, 4)
        self.assertEqual(self.team_of_2.pets[0].health, 2)

    def test_5_v_2(self):
        expected_results = [1, 0]
        results = fight(self.team_of_5, self.team_of_2)
        self.assertEqual(results, expected_results)

    def test_5_v_big(self):
        expected_results = [0, 1]
        results = fight(self.team_of_5, opponent_team)
        self.assertEqual(results, expected_results)

    def test_2_v_5(self):
        expected_results = [0, 1]
        results = fight(self.team_of_2, self.team_of_5)
        self.assertEqual(results, expected_results)

    def test_2_v_big(self):
        expected_results = [0, 1]
        results = fight(self.team_of_2, opponent_team)
        self.assertEqual(results, expected_results)

    def test_big_v_5(self):
        expected_results = [1, 0]
        results = fight(opponent_team, self.team_of_5)
        self.assertEqual(results, expected_results)

    def test_big_v_2(self):
        expected_results = [1, 0]
        results = fight(opponent_team, self.team_of_2)
        self.assertEqual(results, expected_results)

    def test_symmetrical_results(self):
        expected_results = [0, 0]
        for team in self.teams_to_test:
            self.assertEqual(fight(team, team), expected_results)
