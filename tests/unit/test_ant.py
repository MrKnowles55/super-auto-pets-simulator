import unittest

from src.pet_utils.pet import Pet
from src.action_utils.battle import Battle
from src.team_utils.team import Team

from src.data_utils.enums.trigger_event import TriggerEvent
from src.data_utils.enums.trigger_by_kind import TriggerByKind


def create_ant():
    return Pet(name="Ant",
               base_attack=2,
               base_health=1,
               ability={
                   "trigger": TriggerEvent.Faint,
                   "triggered_by": TriggerByKind.Self,
                   "effect": Pet.modify_stats,
                   "effect_dict": {"attackAmount": 2, "healthAmount": 1, "target": Pet.target_random_friend}
               }
               )


def create_dummy(team):
    return Pet(name="Dummy", team=team)


class TestAnt(unittest.TestCase):
    def setUp(self):
        self.player_team = Team("Player")
        self.enemy_team = Team("Enemy")
        print("\n")

    def test_ant_init(self):
        """
        Test pet_utils creation and initialization
        :return:
        """
        expected_values = {
            "name": "Ant",
            "base_attack": 2,
            "base_health": 1,
            "tier": 1,
            "ability": {
                   "trigger": TriggerEvent.Faint,
                   "triggered_by": TriggerByKind.Self,
                   "effect": Pet.modify_stats,
                   "effect_dict": {"attackAmount": 2, "healthAmount": 1, "target": Pet.target_random_friend}
               },
            "level": 1,
            "attack_mod": 0,
            "health_mod": 0,
            "team": None,
            "start_position": -1,
            "position": -1,
            "attack": 2,
            "health": 1
        }

        ant = create_ant()
        for key, value in expected_values.items():
            self.assertEqual(ant.__dict__[key], value)

    def test_ability_no_targets(self):
        ant = create_ant()
        ant2 = create_ant()
        self.player_team.add_pet(ant)
        self.player_team.add_pet(ant2)

        ant3 = create_ant()
        self.enemy_team.add_pet(ant3)

        ant2.ability["triggered_by"] = TriggerByKind.FriendAhead
        ant3.ability["triggered_by"] = TriggerByKind.EachEnemy
        battle = Battle(self.player_team, self.enemy_team)
        ant.broadcast(TriggerEvent.Faint)


