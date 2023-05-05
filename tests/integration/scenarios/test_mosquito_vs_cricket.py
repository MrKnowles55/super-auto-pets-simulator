import unittest
from src.pet.pet_factory import create_pet
from src.battle import fight, start_of_battle, get_pet_list, fight_loop, end_of_battle
from src.team.team import Team, player_team, opponent_team
from src.action.action_utils import action_handler, generate_summon_action, generate_damage_action


class TestMosquitoVsCricket(unittest.TestCase):
    """
    Tests a team of 5 Mosquitoes vs 2 Crickets to ensure Damage Ability and Summon ability follow layering.
    Once the fight starts, 4 mosquitoes should deal damage to the 2 Crickets which have 2 health. The last Mosquito will
    have no valid targets and do nothing. The crickets should faint, then summon their tokens. Now the fight_loop can
    commence ending the fight with 4 Mosquitoes (2/2) against an empty team.
    """
    def setUp(self):
        """
        player_team : Mosquito(2/2), Mosquito(2/2), Mosquito(2/2), Mosquito(2/2), Mosquito(2/2)
        opponent_team : Cricket(1/2), Cricket(1/2), _, _, _
        :return:
        """
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

    @staticmethod
    def get_mode():
        return player_team.pets[0].name

    def test_team_setup(self):
        """
        Checks the setup by checking team sizes, and samples the first pet in each team.
        :return:
        """
        match self.get_mode():
            case "Mosquito":
                self.assertEqual(len(player_team.pets), 5)
                self.assertEqual(len(opponent_team.pets), 2)
                self.assertEqual(len(get_pet_list(player_team, opponent_team)), 7)

                self.assertEqual(player_team.pets[0].name, "Mosquito")
                self.assertEqual(opponent_team.pets[0].name, "Cricket")

                self.assertEqual(player_team.pets[0].attack, 2)
                self.assertEqual(opponent_team.pets[0].attack, 1)
            case "Cricket":
                self.assertEqual(len(player_team.pets), 2)
                self.assertEqual(len(opponent_team.pets), 5)
                self.assertEqual(len(get_pet_list(player_team, opponent_team)), 7)

                self.assertEqual(player_team.pets[0].name, "Cricket")
                self.assertEqual(opponent_team.pets[0].name, "Mosquito")

                self.assertEqual(player_team.pets[0].attack, 1)
                self.assertEqual(opponent_team.pets[0].attack, 2)

    def test_get_pet_list(self):
        """
        Checks the get_pet_list properly combines the two team lists into a single list.
        :return:
        """
        pet_list = get_pet_list(player_team, opponent_team)
        self.assertEqual(len(pet_list), 7)

    def test_fight(self):
        """
        Checks that the Mosquitoes win the fight.
        :return:
        """
        expected_result = [0, 0]
        match self.get_mode():
            case "Mosquito":
                expected_result = [1, 0]
            case "Cricket":
                expected_result = [0, 1]
        result = fight(player_team, opponent_team)
        self.assertEqual(result, expected_result)

    def test_start_of_battle(self):
        """
        Checks that the Mosquitoes properly execute Damage abilities to knockout both Crickets, and do not somehow
        knockout the summoned Zombie Crickets.
        :return:
        """
        pet_list = get_pet_list(player_team, opponent_team)
        match self.get_mode():
            case "Mosquito":
                start_of_battle(player_team, opponent_team, pet_list)
                for pet in opponent_team.pets:
                    self.assertEqual(pet.name, "Zombie Cricket")
                self.assertEqual(len(opponent_team.pets), 2)
            case "Cricket":
                start_of_battle(player_team, opponent_team, pet_list)
                for pet in player_team.pets:
                    self.assertEqual(pet.name, "Zombie Cricket")
                self.assertEqual(len(player_team.pets), 2)

    def test_fight_loop(self):
        """
        Checks that fight_loop ends with 4 Mosquitoes (2/2) and an empty enemy team.
        Simulates the Start of Battle section by applying 2 damage to the crickets, then executing their abilities
        before the fight loop.
        :return:
        """

        match self.get_mode():
            case "Mosquito":
                attacker = player_team.pets[0]
                opponent_team.pets[1].apply_damage(2, attacker)
                opponent_team.pets[0].apply_damage(2, attacker)
                action_handler.execute_actions()
                fight_loop(player_team, opponent_team)
                self.assertEqual(len(opponent_team.pets), 0)
                self.assertEqual(len(player_team.pets), 4)
            case "Cricket":
                attacker = opponent_team.pets[0]
                player_team.pets[1].apply_damage(2, attacker)
                player_team.pets[0].apply_damage(2, attacker)
                action_handler.execute_actions()
                fight_loop(player_team, opponent_team)
                self.assertEqual(len(opponent_team.pets), 4)
                self.assertEqual(len(player_team.pets), 0)

    def test_end_of_battle(self):
        impossible_both_teams_have_pet = end_of_battle(player_team, opponent_team)
        empty_team = Team("Empty")
        player_wins = end_of_battle(player_team, empty_team)
        opponent_wins = end_of_battle(empty_team, opponent_team)
        tie_result = end_of_battle(empty_team, empty_team)
        self.assertEqual(impossible_both_teams_have_pet, [1, 1])
        self.assertEqual(player_wins, [1, 0])
        self.assertEqual(opponent_wins, [0, 1])
        self.assertEqual(tie_result, [0, 0])


class TestCricketVsMosquito(TestMosquitoVsCricket):
    """
    Tests a team of 2 Crickets vs 5 Mosquitoes.
    This class will reuse test methods from TestMosquitoVsCricket with swapped teams.
    """
    def setUp(self):
        """
        player_team : Cricket(1/2), Cricket(1/2), _, _, _
        opponent_team : Mosquito(2/2), Mosquito(2/2), Mosquito(2/2), Mosquito(2/2), Mosquito(2/2)
        :return:
        """
        player_team.pets = [
            create_pet("Cricket"),
            create_pet("Cricket")
        ]

        opponent_team.pets = [
            create_pet("Mosquito"),
            create_pet("Mosquito"),
            create_pet("Mosquito"),
            create_pet("Mosquito"),
            create_pet("Mosquito")
        ]

        # Set the team for each pet in player_team
        for pet in player_team.pets:
            pet.team = player_team

        # Set the team for each pet in opponent_team
        for pet in opponent_team.pets:
            pet.team = opponent_team


if __name__ == '__main__':
    unittest.main()
