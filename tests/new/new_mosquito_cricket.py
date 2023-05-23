import unittest
from actions import PriorityQueue, Action
from pet.new_pet import Pet
from new_battle import Battle
from team.team import Team


def create_mosquito(team):
    return Pet(name="Mosquito",
               base_attack=2,
               base_health=2,
               team=team,
               ability={
                "trigger": "Start of Battle",
                "triggered_by": "Player",
                "effect": Pet.fake_effect,
                "effect_dict": {"damage": 1, "target": Pet.target_fake}
                }
               )


def create_dummy(team):
    return Pet(name="Dummy", team=team)


class TestNewPet(unittest.TestCase):
    def setUp(self) -> None:
        self.player_team = Team("Player")
        self.enemy_team = Team("Enemy")

    def test_mosquito(self):
        # Mosquito vs 1/1
        self.player_team.add_pet(create_mosquito(self.player_team))
        self.enemy_team.add_pet(create_dummy(self.enemy_team))

        battle = Battle(self.player_team, self.enemy_team)

        # Start of battle trigger
        battle.start_of_battle()

        # 1 action in queue
        self.assertEqual(len(battle.action_queue.queue), 1)

        # Queue and Queued Action are correct
        queued_action_tuple = battle.action_queue.queue[0]
        queued_action = queued_action_tuple[2]
        priority = -2
        count = 0.0
        expected_action = {
            "method": Pet.fake_effect,
            "kwargs": {"damage": 1, "target": Pet.target_fake}
        }

        self.assertEqual(priority, queued_action_tuple[0])
        self.assertEqual(count, queued_action_tuple[1])
        self.assertEqual(expected_action["method"], queued_action.method)
        self.assertEqual(expected_action["kwargs"], queued_action.kwargs)

        # Execute Action

        action = battle.action_queue.get_next_action()
        action_results = action.execute()
        self.assertEqual(action_results, expected_action["kwargs"])



