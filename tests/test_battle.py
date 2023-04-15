import unittest
from src.battle import fight


class TestBattle(unittest.TestCase):
    def setUp(self) -> None:
        test_pool = ["Ant"]

        # main(sims=1, friendly_team_size=5, enemy_team_size=5,
        #      friendly_pool=test_pool, enemy_pool=test_pool)
