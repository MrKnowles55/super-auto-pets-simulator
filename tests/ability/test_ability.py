import unittest
from src.pet import Pet
from src.ability.ability_generator import AbilityGenerator
from src.ability.ability import Ability, No_Ability
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

    def test_no_ability_instance_and_trigger_event(self):
        ability = No_Ability(self.test_pet)

        ability.apply(self.test_pet, None)
        self.assertIsNone(ability.trigger_event)
        self.assertIsInstance(ability, Ability)


# Mock Ability class to be used in tests
class MockAbility:
    def __init__(self):
        self.trigger_event = None

    def generate(self):
        return self

    def trigger(self, event, pet, team, enemy_team=None):
        self.trigger_event = event

    def apply(self, pet, team, enemy_team):
        pass


if __name__ == '__main__':
    unittest.main()
