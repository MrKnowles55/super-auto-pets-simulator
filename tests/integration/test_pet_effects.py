import logging
import unittest
from math import floor
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


class TestPet_Effect(unittest.TestCase):
    def setUp(self) -> None:
        self.player_team = Team("Player")
        self.enemy_team = Team("Enemy")
        self.battle = Battle(self.player_team, self.enemy_team)

        self.pet = Pet('test')
        self.player_team.add_pet(self.pet)

        print("\n")

    # Perk
    def test_apply_status(self):
        pass

    # Damage

    def test_deal_damage(self):
        # Target Self
        # deal 1 damage, then  -1 and 0.5 damage (which round to 0)
        self.pet.base_health = 2
        self.pet.deal_damage(target=EffectTargetKind.Self, amount=1)
        self.pet.deal_damage(target=EffectTargetKind.Self, amount=-1)
        self.pet.deal_damage(target=EffectTargetKind.Self, amount=0.5)
        self.assertEqual(self.pet.health, 1)
        self.assertEqual(self.pet.damage, 1)

        # Target All, with attack_damage_percent
        fill_team(self.player_team, 5)
        fill_team(self.enemy_team, 5)
        self.player_team.first.base_attack = 10
        self.enemy_team.first.base_health = 10
        self.player_team.first.deal_damage(target=EffectTargetKind.All, amount={"attack_damage_percent": 50})
        self.assertEqual(self.player_team.length, 0)
        self.assertEqual(self.enemy_team.length, 1)
        self.assertEqual(self.enemy_team.first.health, 5)

        # TODO test percentage

    # Food
    def test_food_multiplier(self):
        pass

    # Level and Experience

    def test_evolve(self):
        pass
        # for lvl in range(1, 4):
        #     self.assertEqual(self.pet.level, lvl)
        #     self.assertEqual(self.pet.base_health, lvl)
        #     self.assertEqual(self.pet.base_attack, lvl)
        #     self.pet.evolve(target=EffectTargetKind.Self)

    def test_gain_experience(self):

        while self.pet.level < 3:
            self.pet.gain_experience(target=EffectTargetKind.Self)

        self.assertEqual(self.pet.level, 3)
        self.assertEqual(self.pet.experience, 0)
        self.assertEqual(self.pet.base_health, 6)
        self.assertEqual(self.pet.base_attack, 6)
        self.assertEqual(self.pet.ability, self.pet.ability_by_level[3])

    # Gold and Other Currency

    def test_gain_gold(self):
        pass

    def test_roll_modifier(self):
        pass

    def test_conserve_gold(self):
        pass

    def test_gain_trumpets(self):
        pass

    # Buff / Nerf

    def test_modify_stats(self):
        self.pet.modify_stats(target=EffectTargetKind.Self, attack_mod=1)
        self.assertEqual(self.pet.attack_mod, 1)
        self.pet.damage = 1
        self.pet.base_health = 2
        for mod in range(-5, 1):
            self.pet.attack_mod = 0
            self.pet.health_mod = 0
            self.pet.modify_stats(target=EffectTargetKind.Self, attack_mod=mod, health_mod=mod)
            self.assertEqual(self.pet.attack, 1 + mod)
            self.assertEqual(self.pet.health, max(1 + mod, 1))

    # for percent in [30, 33, 50, 60, 66, 90, 100, 150]:

    def test_reduce_health(self):
        self.pet.base_health = 50
        for hp in range(1, 50):
            for percent in [33, 66, 100]:
                self.pet.base_health = hp
                self.pet.damage = self.pet.health - 1
                self.pet.health_mod = 0
                self.pet.reduce_health(target=EffectTargetKind.Self, health_mod=percent)
                print(
                    f"{percent}%  {self.pet.health} = {self.pet.base_health} + {self.pet.health_mod} - {self.pet.damage}")
                # self.assertEqual(self.pet.health, int(max(self.pet.health * (100-percent)/100, 1)))

    # Shop

    def test_refill_shops(self):
        pass

    def test_discount_food(self):
        pass

    def test_modify_shop(self):
        pass

    # Transfer

    def test_repeat_ability(self):
        pass

    def test_transfer_stats(self):
        fill_team(self.enemy_team, 1)
        base_kwargs = {"from": {"kind": EffectTargetKind.Self},
                       "to": {"kind": EffectTargetKind.EachEnemy},
                       "copy_attack": True,
                       "copy_health": True,
                       "percentage": 100}
        self.pet.base_attack = 20
        self.pet.base_health = 10

        for attack_flag in [False, True]:
            for health_flag in [False, True]:
                for percentage in [30, 33, 50, 66, 90, 100, 150]:
                    kwargs = base_kwargs
                    kwargs["copy_attack"] = attack_flag
                    kwargs["copy_health"] = health_flag
                    kwargs["percentage"] = percentage
                    self.enemy_team.first.attack_mod = 0
                    self.enemy_team.first.health_mod = 0

                    self.pet.transfer_stats(**kwargs)

                    self.assertEqual(self.enemy_team.first.attack_mod,
                                     floor(attack_flag * percentage * self.pet.base_attack / 100))
                    self.assertEqual(self.enemy_team.first.health_mod,
                                     floor(health_flag * percentage * self.pet.base_health / 100))

    def test_transfer_ability(self):
        pass

    def test_steal_food(self):
        pass

    # Summon

    def test_summon_pet(self):
        # summon 5 flies to each team
        kwargs = {'pet': "pet-zombie-fly",
                  'team': "Friendly",
                  'base_attack': 2,
                  'base_health': 5,
                  'n': 5}
        self.pet.summon_pet(**kwargs)
        kwargs["team"] = "Enemy"
        self.pet.summon_pet(**kwargs)

        # Audit the players first fly, ensuring indexing is correct as well as stats
        self.assertEqual(self.player_team.first.id, 4)
        self.assertEqual(self.player_team.first.base_attack, kwargs.get("base_attack"))
        self.assertEqual(self.player_team.first.base_health, kwargs.get("base_health"))

        # Audit Enemy team
        self.assertEqual(self.enemy_team.first.id, 10)
        self.assertEqual(self.enemy_team.length, 5)

    def test_summon_random_pet(self):
        pass

    # Special

    def test_swallow(self):
        pass

    def test_move(self):
        pass

    def test_activate_ability(self):
        pass
