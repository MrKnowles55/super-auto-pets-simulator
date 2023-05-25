import unittest

from src.pet_utils.pet_factory import create_pet
from data.old.depreciated.battle import start_of_battle
from data.old.depreciated.team import Team
from data.old.depreciated.action_utils import action_handler

from src.config_utils.logger import setup_logger, log_call

log = setup_logger(__name__)


class TestMosquitoVsCricket(unittest.TestCase):

    def setUp(self):
        self.handler = action_handler
        self.handler.clear_actions()
        self.teams = {}
        print()

    def create_team(self, team_name, pet_names):
        team = Team(team_name)
        pets = {pet_name: [] for pet_name in pet_names}

        for pet_name in pet_names:
            pet = create_pet(pet_name)
            team.add_pet(pet)
            pets[pet_name].append(pet)

        self.teams[team_name] = {"team_utils": team, "pets": pets}

    @log_call(log)
    def test1_Mosquito_v_1_Cricket(self):
        """
        Mosquito does 1 Damage to Cricket
        """
        self.create_team("A", ["mosquito"])
        self.create_team("B", ["cricket"])

        start_of_battle(self.teams["A"]["team_utils"], self.teams["B"]["team_utils"])
        self.handler.execute_actions()

        # Both pets still alive
        self.assertTrue(self.teams["A"]["team_utils"].pets_list)
        self.assertTrue(self.teams["B"]["team_utils"].pets_list)

        # Cricket is hurt
        first_cricket = self.teams["B"]["pets"]["cricket"][0]
        self.assertEqual(first_cricket.health, 1)

    @log_call(log)
    def test2_Mosquito_v_1_Cricket(self):
        """
        2 Mosquitos damage and knockout the Cricket, which then summons a Zombie Cricket
        """
        self.create_team("A", ["mosquito", "mosquito"])
        self.create_team("B", ["cricket"])

        start_of_battle(self.teams["A"]["team_utils"], self.teams["B"]["team_utils"])
        self.handler.execute_actions()

        # 2 Mosquitos and 1 Zombie Cricket
        self.assertEqual(self.teams["A"]["team_utils"].length, 2)
        self.assertEqual(self.teams["B"]["team_utils"].length, 1)

        # Cricket is fainted
        first_cricket = self.teams["B"]["pets"]["cricket"][0]
        self.assertEqual(first_cricket.health, 0)
        self.assertFalse(first_cricket.is_alive)

        # Zombie Cricket summoned
        self.assertEqual(self.teams["B"]["team_utils"].first.name, "Zombie Cricket")

    @log_call(log)
    def test4_Mosquito_v_1_Cricket_Sequentially(self):
        self.create_team("A", ["mosquito", "mosquito", "mosquito", "mosquito"])
        self.create_team("B", ["cricket"])

        self.teams["A"]["team_utils"].pets_list[0].attack = 4
        self.teams["A"]["team_utils"].pets_list[1].attack = 3
        self.teams["A"]["team_utils"].pets_list[2].attack = 2
        self.teams["A"]["team_utils"].pets_list[3].attack = 1

        start_of_battle(self.teams["A"]["team_utils"], self.teams["B"]["team_utils"])
        self.handler.execute_actions()
        print(self.teams["A"]["pets"])



    # def test4_Mosquito_v_2_Cricket(self):
    #     """
    #     4 Mosquitos damage and knockout 2 Crickets, which then summons 2 Zombie Crickets
    #     """
    #     self.create_team("A", ["mosquito", "mosquito", "mosquito", "mosquito"])
    #     self.create_team("B", ["cricket", "cricket"])
    #
    #     start_of_battle(self.teams["A"]["team_utils"], self.teams["B"]["team_utils"])
    #     self.handler.execute_actions()
    #
    #     # 4 Mosquitos and 2 Zombie Cricket
    #     self.assertEqual(self.teams["A"]["team_utils"].length, 4)
    #     self.assertEqual(self.teams["B"]["team_utils"].length, 2)
    #
    #     # Crickets are fainted
    #     self.assertEqual(self.teams["B"]["pets"]["cricket"][0].health, 0)
    #     self.assertFalse(self.teams["B"]["pets"]["cricket"][0].is_alive)
    #
    #     self.assertEqual(self.teams["B"]["pets"]["cricket"][1].health, 0)
    #     self.assertFalse(self.teams["B"]["pets"]["cricket"][1].is_alive)
    #
    #     # Zombie Crickets summoned
    #     self.assertEqual(self.teams["B"]["team_utils"].first.name, "Zombie Cricket")
    #     self.assertEqual(self.teams["B"]["team_utils"].pets_list[1].name, "Zombie Cricket")
    #
    # def test4_Mosquito_v_1_Cricket(self):
    #     team_a = Team("A")
    #     first_mosq = create_pet("mosquito")
    #     second_mosq = create_pet("mosquito")
    #     third_mosq = create_pet("mosquito")
    #     fourth_mosq = create_pet("mosquito")
    #     team_a.add_pet(first_mosq)
    #     team_a.add_pet(second_mosq)
    #     team_a.add_pet(third_mosq)
    #     team_a.add_pet(fourth_mosq)
    #
    #     team_b = Team("B")
    #     first_cricket = create_pet("cricket")
    #     team_b.add_pet(first_cricket)
    #     start_of_battle(team_a, team_b)
    #
    #     self.handler.execute_actions()
    #
    #     # Team A has 1 pets and Team B has 2
    #     self.assertEqual(team_a.length, 1)
    #     self.assertEqual(team_b.length, 2)
    #
    #     # Cricket fainted
    #     self.assertEqual(first_cricket.health, 0)
    #     self.assertFalse(first_cricket.is_alive)
    #
    #     # Zombie Cricket exists and is at full health
    #     self.assertEqual(team_a.pets_list[0].name, "Zombie Cricket")
    #     self.assertEqual(team_a.first.health, 1)
    #     self.assertTrue(team_a.first.isalive)



# import unittest
# from src.pet_utils.pet_factory import create_pet
# from src.battle import fight, start_of_battle, get_pet_list, fight_loop, end_of_battle
# from src.team_utils.team_utils import Team, player_team, opponent_team
# from src.action_utils.action_utils import action_handler, generate_summon_action, generate_damage_action
#
#
# class TestMosquitoVsCricket(unittest.TestCase):
#     """
#     Tests a team_utils of 5 Mosquitoes vs 2 Crickets to ensure Damage Ability and Summon ability follow layering.
#     Once the fight starts, 4 mosquitoes should deal damage to the 2 Crickets which have 2 health. The last Mosquito will
#     have no valid targets and do nothing. The crickets should faint, then summon their tokens. Now the fight_loop can
#     commence ending the fight with 4 Mosquitoes (2/2) against an empty team_utils.
#     """
#     def setUp(self):
#         """
#         player_team : Mosquito(2/2), Mosquito(2/2), Mosquito(2/2), Mosquito(2/2), Mosquito(2/2)
#         opponent_team : Cricket(1/2), Cricket(1/2), _, _, _
#         :return:
#         """
#         player_team.pets_list = [
#             create_pet("Mosquito"),
#             create_pet("Mosquito"),
#             create_pet("Mosquito"),
#             create_pet("Mosquito"),
#             create_pet("Mosquito")
#         ]
#
#         opponent_team.pets_list = [
#             create_pet("Cricket"),
#             create_pet("Cricket")
#         ]
#
#         # Set the team_utils for each pet_utils in player_team
#         for pet_utils in player_team.pets_list:
#             pet_utils.team_utils = player_team
#
#         # Set the team_utils for each pet_utils in opponent_team
#         for pet_utils in opponent_team.pets_list:
#             pet_utils.team_utils = opponent_team
#
#     @staticmethod
#     def get_mode():
#         return player_team.pets_list[0].name
#
#     def test_team_setup(self):
#         """
#         Checks the setup by checking team_utils sizes, and samples the first pet_utils in each team_utils.
#         :return:
#         """
#         match self.get_mode():
#             case "Mosquito":
#                 self.assertEqual(len(player_team.pets_list), 5)
#                 self.assertEqual(len(opponent_team.pets_list), 2)
#                 self.assertEqual(len(get_pet_list(player_team, opponent_team)), 7)
#
#                 self.assertEqual(player_team.pets_list[0].name, "Mosquito")
#                 self.assertEqual(opponent_team.pets_list[0].name, "Cricket")
#
#                 self.assertEqual(player_team.pets_list[0].attack, 2)
#                 self.assertEqual(opponent_team.pets_list[0].attack, 1)
#             case "Cricket":
#                 self.assertEqual(len(player_team.pets_list), 2)
#                 self.assertEqual(len(opponent_team.pets_list), 5)
#                 self.assertEqual(len(get_pet_list(player_team, opponent_team)), 7)
#
#                 self.assertEqual(player_team.pets_list[0].name, "Cricket")
#                 self.assertEqual(opponent_team.pets_list[0].name, "Mosquito")
#
#                 self.assertEqual(player_team.pets_list[0].attack, 1)
#                 self.assertEqual(opponent_team.pets_list[0].attack, 2)
#
#     def test_get_pet_list(self):
#         """
#         Checks the get_pet_list properly combines the two team_utils lists into a single list.
#         :return:
#         """
#         pet_list = get_pet_list(player_team, opponent_team)
#         self.assertEqual(len(pet_list), 7)
#
#     def test_fight(self):
#         """
#         Checks that the Mosquitoes win the fight.
#         :return:
#         """
#         expected_result = [0, 0]
#         match self.get_mode():
#             case "Mosquito":
#                 expected_result = [1, 0]
#             case "Cricket":
#                 expected_result = [0, 1]
#         result = fight(player_team, opponent_team)
#         self.assertEqual(result, expected_result)
#
#     def test_start_of_battle(self):
#         """
#         Checks that the Mosquitoes properly execute Damage abilities to knockout both Crickets, and do not somehow
#         knockout the summoned Zombie Crickets.
#         :return:
#         """
#         pet_list = get_pet_list(player_team, opponent_team)
#         match self.get_mode():
#             case "Mosquito":
#                 start_of_battle(player_team, opponent_team, pet_list)
#                 for pet_utils in opponent_team.pets_list:
#                     self.assertEqual(pet_utils.name, "Zombie Cricket")
#                 self.assertEqual(len(opponent_team.pets_list), 2)
#             case "Cricket":
#                 start_of_battle(player_team, opponent_team, pet_list)
#                 for pet_utils in player_team.pets_list:
#                     self.assertEqual(pet_utils.name, "Zombie Cricket")
#                 self.assertEqual(len(player_team.pets_list), 2)
#
#     def test_fight_loop(self):
#         """
#         Checks that fight_loop ends with 4 Mosquitoes (2/2) and an empty enemy team_utils.
#         Simulates the Start of Battle section by applying 2 damage to the crickets, then executing their abilities
#         before the fight loop.
#         :return:
#         """
#
#         match self.get_mode():
#             case "Mosquito":
#                 attacker = player_team.pets_list[0]
#                 opponent_team.pets_list[1].apply_damage(2, attacker)
#                 opponent_team.pets_list[0].apply_damage(2, attacker)
#                 action_handler.execute_actions()
#                 fight_loop(player_team, opponent_team)
#                 self.assertEqual(len(opponent_team.pets_list), 0)
#                 self.assertEqual(len(player_team.pets_list), 4)
#             case "Cricket":
#                 attacker = opponent_team.pets_list[0]
#                 player_team.pets_list[1].apply_damage(2, attacker)
#                 player_team.pets_list[0].apply_damage(2, attacker)
#                 action_handler.execute_actions()
#                 fight_loop(player_team, opponent_team)
#                 self.assertEqual(len(opponent_team.pets_list), 4)
#                 self.assertEqual(len(player_team.pets_list), 0)
#
#     def test_end_of_battle(self):
#         impossible_both_teams_have_pet = end_of_battle(player_team, opponent_team)
#         empty_team = Team("Empty")
#         player_wins = end_of_battle(player_team, empty_team)
#         opponent_wins = end_of_battle(empty_team, opponent_team)
#         tie_result = end_of_battle(empty_team, empty_team)
#         self.assertEqual(impossible_both_teams_have_pet, [1, 1])
#         self.assertEqual(player_wins, [1, 0])
#         self.assertEqual(opponent_wins, [0, 1])
#         self.assertEqual(tie_result, [0, 0])
#
#
# class TestCricketVsMosquito(TestMosquitoVsCricket):
#     """
#     Tests a team_utils of 2 Crickets vs 5 Mosquitoes.
#     This class will reuse test methods from TestMosquitoVsCricket with swapped teams.
#     """
#     def setUp(self):
#         """
#         player_team : Cricket(1/2), Cricket(1/2), _, _, _
#         opponent_team : Mosquito(2/2), Mosquito(2/2), Mosquito(2/2), Mosquito(2/2), Mosquito(2/2)
#         :return:
#         """
#         player_team.pets_list = [
#             create_pet("Cricket"),
#             create_pet("Cricket")
#         ]
#
#         opponent_team.pets_list = [
#             create_pet("Mosquito"),
#             create_pet("Mosquito"),
#             create_pet("Mosquito"),
#             create_pet("Mosquito"),
#             create_pet("Mosquito")
#         ]
#
#         # Set the team_utils for each pet_utils in player_team
#         for pet_utils in player_team.pets_list:
#             pet_utils.team_utils = player_team
#
#         # Set the team_utils for each pet_utils in opponent_team
#         for pet_utils in opponent_team.pets_list:
#             pet_utils.team_utils = opponent_team
#
#
# if __name__ == '__main__':
#     unittest.main()
