import unittest
from src.pet.pet_entity import PetEntity
from src.ability.ability_generator import AbilityGenerator
from src.ability.ability_abstract import AbilityBase, No_Ability
from src.team.team import Team


class TestAbility(unittest.TestCase):

    def setUp(self):
        self.test_pet = PetEntity(name="Test Pet", attack=1, health=1, tier=1, level=1,
                                  ability1=None, ability2=None, ability3=None, ability_generator=AbilityGenerator)
        self.test_team = Team("Test")
        self.test_team.add_pet(self.test_pet)

        # self.friend_pet1 = PetEntity(name="Test Friend Pet 1", attack=1, health=1, tier=1, level=1,
        #                              ability1=None, ability2=None, ability3=None, ability_generator=AbilityGenerator)
        # self.friend_pet2 = PetEntity(name="Test Friend Pet 2", attack=1, health=1, tier=1, level=1,
        #                              ability1=None, ability2=None, ability3=None, ability_generator=AbilityGenerator)

        # self.test_team.add_pet(self.friend_pet1)
        # self.test_team.add_pet(self.friend_pet2)

    def test_no_ability_instance_and_trigger_event(self):
        ability = No_Ability(self.test_pet)

        ability.apply()
        self.assertIsNone(ability.trigger_event)
        self.assertIsInstance(ability, AbilityBase)


if __name__ == '__main__':
    unittest.main()
