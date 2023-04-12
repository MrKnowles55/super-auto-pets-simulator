import unittest
from src.pet import Pet
from src.ability.ability_generator import AbilityGenerator
from src.ability.ability import Ability
from src.ability.modify_stats import ModifyStatsAbilityRandomFriend
from src.pet_data_utils.enums.trigger_event import TriggerEvent
from src.pet_data_utils.enums.effect_kind import EffectKind
from src.pet_data_utils.enums.effect_target_kind import EffectTargetKind
from src.team.team import Team


class TestAbility(unittest.TestCase):

    def setUp(self):
        self.test_pet = Pet(name="Test Pet", attack=1, health=1, tier=1, level=1,
                            ability1=None, ability2=None, ability3=None, ability_generator=AbilityGenerator)
        self.friend_pet1 = Pet(name="Test Friend Pet 1", attack=1, health=1, tier=1, level=1,
                               ability1=None, ability2=None, ability3=None, ability_generator=AbilityGenerator)
        self.friend_pet2 = Pet(name="Test Friend Pet 2", attack=1, health=1, tier=1, level=1,
                               ability1=None, ability2=None, ability3=None, ability_generator=AbilityGenerator)
        self.test_team = Team()
        self.test_team.add_pet(self.test_pet)
        self.test_team.add_pet(self.friend_pet1)
        self.test_team.add_pet(self.friend_pet2)

    def test_modify_stats_ability_random_friend_attributes(self):
        ability = ModifyStatsAbilityRandomFriend(owner=self.test_pet, attack_mod=1, health_mod=1,
                                                 target_type=EffectTargetKind.RandomFriend, target_n=2,
                                                 trigger_event=TriggerEvent.StartOfBattle, until_end_of_battle=True)

        self.assertIsInstance(ability, Ability)
        self.assertIn(ability.target_type, EffectTargetKind)
        self.assertIn(ability.trigger_event, TriggerEvent)

    def test_modify_stats_ability_random_friend_apply(self):
        ability = ModifyStatsAbilityRandomFriend(owner=self.test_pet, attack_mod=1, health_mod=1,
                                                 target_type=EffectTargetKind.RandomFriend, target_n=2,
                                                 trigger_event=TriggerEvent.StartOfBattle, until_end_of_battle=True)

        ability.trigger(event=TriggerEvent.StartOfBattle, pet=self.test_pet, team=self.test_team)

        self.assertEqual(self.friend_pet1.attack, 2)
        self.assertEqual(self.friend_pet1.health, 2)
        self.assertEqual(self.friend_pet1.attack, self.friend_pet2.attack)


if __name__ == '__main__':
    unittest.main()
