import unittest
from pet_factory import create_pet
from battle import fight, start_of_battle, get_pet_list, fight_loop, end_of_battle
from src.team.team import Team, player_team, opponent_team


class TestScenario(unittest.TestCase):
    def setUp(self):
        player_team.pets = [
            create_pet("Mosquito"),
            create_pet("Mosquito"),
            create_pet("Mosquito"),
            create_pet("Mosquito"),
            create_pet("Mosquito")
        ]

        opponent_team.pets = [
            create_pet("Cricket"),
            create_pet("Cricket")
        ]

        # Set the team for each pet in player_team
        for pet in player_team.pets:
            pet.team = player_team

        # Set the team for each pet in opponent_team
        for pet in opponent_team.pets:
            pet.team = opponent_team

    def test_team_setup(self):
        self.assertEqual(len(player_team.pets), 5)
        self.assertEqual(len(opponent_team.pets), 2)
        self.assertEqual(len(get_pet_list(player_team, opponent_team)), 7)

        self.assertEqual(player_team.pets[0].name, "Mosquito")
        self.assertEqual(opponent_team.pets[0].name, "Cricket")

        self.assertEqual(player_team.pets[0].attack, 2)
        self.assertEqual(opponent_team.pets[0].attack, 1)

    def test_get_pet_list(self):
        pet_list = get_pet_list(player_team, opponent_team)
        self.assertEqual(len(pet_list), 7)

    def test_fight(self):
        result = fight(player_team, opponent_team)
        self.assertEqual(result[0], 1)

    def test_start_of_battle(self):
        pet_list = get_pet_list(player_team, opponent_team)
        start_of_battle(player_team, opponent_team, pet_list, verbose=True)
        for pet in opponent_team.pets:
            self.assertEqual(pet.name, "Zombie Cricket")
        self.assertEqual(len(opponent_team.pets), 2)

    def test_fight_loop(self):
        fight_loop(player_team, opponent_team)
        print(player_team.pets)
        self.assertEqual(len(opponent_team.pets), 0)
        self.assertEqual(len(player_team.pets), 4)


if __name__ == '__main__':
    unittest.main()
