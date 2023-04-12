import unittest
from src.pet import Pet
from tests.team.test_teams import MockTeam
from tests.ability.test_ability import MockAbility
from src.pet_data_utils.enums.trigger_event import TriggerEvent
from src.pet_data_utils.enums.effect_kind import EffectKind
from src.pet_data_utils.enums.effect_target_kind import EffectTargetKind


class TestPet(unittest.TestCase):
    def setUp(self):
        self.pet = Pet(name="Test Pet", attack=5, health=10, tier=1, level=1, ability1=None, ability2=None,
                       ability3=None, ability_generator=lambda *_: MockAbility())
        self.enemy_pet = Pet(name="Enemy Pet", attack=3, health=7, tier=1, level=1, ability1=None, ability2=None,
                             ability3=None, ability_generator=lambda *_: MockAbility())

        self.pet_team = MockTeam()
        self.enemy_team = MockTeam()

        self.pet.team = self.pet_team
        self.enemy_pet.team = self.enemy_team

        self.pet_team.pets.append(self.pet)
        self.enemy_team.pets.append(self.enemy_pet)

    def test_initial_values(self):
        self.assertEqual(self.pet.attack, 5)
        self.assertEqual(self.pet.health, 10)
        self.assertFalse(self.pet.fainted)

    def test_is_alive(self):
        self.assertTrue(self.pet.is_alive())

    def test_attack_pet(self):
        self.pet.attack_pet(self.enemy_pet)
        self.assertEqual(self.pet.health, 7)
        self.assertEqual(self.enemy_pet.health, 2)

    def test_faint(self):
        self.pet.health = 0
        self.pet.faint()
        self.assertTrue(self.pet.fainted)

    def test_start_of_battle(self):
        self.pet.start_of_battle(self.enemy_team)
        self.assertEqual(self.pet.ability.trigger_event, TriggerEvent.StartOfBattle)

    def test_hurt(self):
        self.pet.health = 5
        self.pet.hurt()
        self.assertEqual(self.pet.ability.trigger_event, TriggerEvent.Hurt)

    def test_before_attack(self):
        self.pet.before_attack()
        self.assertEqual(self.pet.ability.trigger_event, TriggerEvent.BeforeAttack)


if __name__ == '__main__':
    unittest.main()
