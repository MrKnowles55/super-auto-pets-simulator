# import unittest
# from src.pet.pet_factory import create_pet
# from src.battle import fight
# from src.team.team import Team
# from src.action.action_utils import action_handler
# from src.config_utils.logger import setup_logger, log_call, log_class_init
# # Flamingo object data
# """
#     "pet-flamingo": {
#         "name": "Flamingo",
#         "id": "pet-flamingo",
#         "image": {
#             "source": "noto-emoji",
#             "commit": "e022fd6573782431ac9a65b520376b57511c31cd",
#             "unicodeCodePoint": "\ud83e\udda9"
#         },
#         "tier": 2,
#         "baseAttack": 4,
#         "baseHealth": 2,
#         "packs": [
#             "Turtle",
#             "Puppy"
#         ],
#         "level1Ability": {
#             "description": "Faint: Give the two friends behind +1/+1.",
#             "trigger": "Faint",
#             "triggeredBy": {
#                 "kind": "Self"
#             },
#             "effect": {
#                 "kind": "ModifyStats",
#                 "target": {
#                     "kind": "FriendBehind",
#                     "n": 2
#                 },
#                 "attackAmount": 1,
#                 "healthAmount": 1,
#                 "untilEndOfBattle": false
#             }
#         },
#         "level2Ability": {
#             "description": "Faint: Give the two friends behind +2/+2.",
#             "trigger": "Faint",
#             "triggeredBy": {
#                 "kind": "Self"
#             },
#             "effect": {
#                 "kind": "ModifyStats",
#                 "target": {
#                     "kind": "FriendBehind",
#                     "n": 2
#                 },
#                 "attackAmount": 2,
#                 "healthAmount": 2,
#                 "untilEndOfBattle": false
#             }
#         },
#         "level3Ability": {
#             "description": "Faint: Give the two friends behind +3/+3.",
#             "trigger": "Faint",
#             "triggeredBy": {
#                 "kind": "Self"
#             },
#             "effect": {
#                 "kind": "ModifyStats",
#                 "target": {
#                     "kind": "FriendBehind",
#                     "n": 2
#                 },
#                 "attackAmount": 3,
#                 "healthAmount": 3,
#                 "untilEndOfBattle": false
#             }
#         },"""
#
# log = setup_logger(__name__)
#
#
# @log_class_init(log)
# class TestFlamingo(unittest.TestCase):
#
#     @log_call(log)
#     def setUp(self) -> None:
#
#         self.team_of_5_flamingos = Team("5 Flamingos")
#         self.team_of_2_flamingos = Team("2 Flamingos")
#         self.team_of_5_big_guys = Team("5 Big Guys")
#
#         self.team_of_5_flamingos.add_pet(create_pet("Flamingo"))
#         self.team_of_5_flamingos.add_pet(create_pet("Flamingo"))
#         self.team_of_5_flamingos.add_pet(create_pet("Flamingo"))
#         self.team_of_5_flamingos.add_pet(create_pet("Flamingo"))
#         self.team_of_5_flamingos.add_pet(create_pet("Flamingo"))
#
#         self.team_of_2_flamingos.add_pet(create_pet("Flamingo"))
#         self.team_of_2_flamingos.add_pet(create_pet("Flamingo"))
#
#         self.team_of_5_big_guys.add_pet(create_pet("Big Test"))
#         self.team_of_5_big_guys.add_pet(create_pet("Big Test"))
#         self.team_of_5_big_guys.add_pet(create_pet("Big Test"))
#         self.team_of_5_big_guys.add_pet(create_pet("Big Test"))
#         self.team_of_5_big_guys.add_pet(create_pet("Big Test"))
#
#         self.teams_to_test = [self.team_of_5_flamingos, self.team_of_2_flamingos, self.team_of_5_big_guys]
#
#         # Store the initial pets for each team
#         self.initial_pets = {
#             self.team_of_5_flamingos.name: self.team_of_5_flamingos.pets_list[:],
#             self.team_of_2_flamingos.name: self.team_of_2_flamingos.pets_list[:],
#             self.team_of_5_big_guys.name: self.team_of_5_big_guys.pets_list[:]
#         }
#
#     @log_call(log)
#     def test_team_setup(self):
#
#         # Check team sizes
#         self.assertEqual(len(self.team_of_5_flamingos.pets_list), 5)
#         self.assertEqual(len(self.team_of_2_flamingos.pets_list), 2)
#         self.assertEqual(len(self.team_of_5_big_guys.pets_list), 5)
#
#         # Check teams have correct pets
#         team_to_pet_dict = {
#             self.team_of_5_flamingos: ["Flamingo", 4],  # name and attack
#             self.team_of_2_flamingos: ["Flamingo", 4],
#             self.team_of_5_big_guys: ["Big Test", 50]
#         }
#         for team in self.teams_to_test:
#             for pet in team.pets_list:
#                 self.assertEqual(pet.name, team_to_pet_dict[team][0])
#                 self.assertEqual(pet.attack, team_to_pet_dict[team][1])
#
#     @log_call(log)
#     def test_first_flamingo_faints_with_2_friends_behind_get_buffed(self):
#
#         # Knockout first Flamingo
#         attacker = self.team_of_5_big_guys.pets_list[0]
#         self.team_of_5_flamingos.pets_list[0].apply_damage(50, attacker)
#
#         # check that Flamingo fainted
#         self.assertEqual(len(self.team_of_5_flamingos.pets_list), 4)
#
#         # Action execution
#         action_handler.execute_actions()
#
#         # Check that the first 2 Flamingos behind the fainted one gain +1/+1
#         self.assertEqual(self.team_of_5_flamingos.pets_list[0].attack, 5)
#         self.assertEqual(self.team_of_5_flamingos.pets_list[0].health, 3)
#         self.assertEqual(self.team_of_5_flamingos.pets_list[1].attack, 5)
#         self.assertEqual(self.team_of_5_flamingos.pets_list[1].health, 3)
#
#         # Check that last 2 Flamingos did not have stats modified
#         self.assertEqual(self.team_of_5_flamingos.pets_list[2].attack, 4)
#         self.assertEqual(self.team_of_5_flamingos.pets_list[2].health, 2)
#         self.assertEqual(self.team_of_5_flamingos.pets_list[3].attack, 4)
#         self.assertEqual(self.team_of_5_flamingos.pets_list[3].health, 2)
#
#     @log_call(log)
#     def test_second_to_last_flamingo_faints_with_one_friend_behind_buffed(self):
#         attacker = self.team_of_5_big_guys.pets_list[0]
#         self.team_of_5_flamingos.pets_list[3].apply_damage(50, attacker)
#
#         self.assertEqual(len(self.team_of_5_flamingos.pets_list), 4)
#
#         # Action execution
#         action_handler.execute_actions()
#
#         self.assertEqual(self.team_of_5_flamingos.pets_list[0].attack, 4)
#         self.assertEqual(self.team_of_5_flamingos.pets_list[0].health, 2)
#
#         self.assertEqual(self.team_of_5_flamingos.pets_list[1].attack, 4)
#         self.assertEqual(self.team_of_5_flamingos.pets_list[1].health, 2)
#
#         self.assertEqual(self.team_of_5_flamingos.pets_list[2].attack, 4)
#         self.assertEqual(self.team_of_5_flamingos.pets_list[2].health, 2)
#
#         self.assertEqual(self.team_of_5_flamingos.pets_list[3].attack, 5)
#         self.assertEqual(self.team_of_5_flamingos.pets_list[3].health, 3)
#
#     @log_call(log)
#     def test_last_flamingo_faints_buffs_none(self):
#         attacker = self.team_of_5_big_guys.pets_list[0]
#         self.team_of_5_flamingos.pets_list[1].apply_damage(50, attacker)
#
#         self.assertEqual(len(self.team_of_5_flamingos.pets_list), 4)
#
#         # Action execution
#         action_handler.execute_actions()
#
#         self.assertEqual(self.team_of_5_flamingos.pets_list[0].attack, 4)
#         self.assertEqual(self.team_of_5_flamingos.pets_list[0].health, 2)
#
#     @log_call(log)
#     def test_flamingo_faints_no_friends(self):
#
#         # remove all the flamingos friends
#         while len(self.team_of_5_flamingos.pets_list) > 1:
#             self.team_of_5_flamingos.remove_pet(self.team_of_5_flamingos.pets_list[0])
#
#         attacker = self.team_of_5_big_guys.pets_list[0]
#         self.team_of_5_flamingos.pets_list[0].apply_damage(50, attacker)
#
#         self.assertFalse(self.team_of_5_flamingos.pets_list)
#
#     @log_call(log)
#     def test_first_2_flamingo_faints_simultaneously_with_friends_behind(self):
#         print(self.team_of_5_flamingos.pets_list)
#         attacker = self.team_of_5_big_guys.pets_list[0]
#         self.team_of_5_flamingos.pets_list[0].apply_damage(50, attacker)
#         print(self.team_of_5_flamingos.pets_list)
#         self.team_of_5_flamingos.pets_list[0].apply_damage(50, attacker)
#         print(self.team_of_5_flamingos.pets_list)
#         self.team_of_5_flamingos.pets_list[0].apply_damage(50, attacker)
#         print(self.team_of_5_flamingos.pets_list)
#
#         self.assertEqual(len(self.team_of_5_flamingos.pets_list), 2)
#         # Action execution
#         action_handler.execute_actions()
#
#         print(self.team_of_5_flamingos.pets_list)
