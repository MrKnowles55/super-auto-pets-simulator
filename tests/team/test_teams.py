import unittest
from pet.pet_entity import PetEntity
from src.ability.ability_generator import AbilityGenerator
from src.team.team import Team


class TestTeam(unittest.TestCase):

    def test_add_pet(self):
        team = Team("Test")
        pet = PetEntity("Test Pet", 5, 10, 1, 1, None, None, None, AbilityGenerator)

        team.add_pet(pet)
        self.assertIn(pet, team.pets)

    def test_remove_pet(self):
        team = Team("Test")
        pet = PetEntity("Test Pet", 5, 10, 1, 1, None, None, None, AbilityGenerator)

        team.add_pet(pet)
        team.remove_pet(pet)
        self.assertNotIn(pet, team.pets)

    def test_move_pet(self):
        team = Team("Test")
        pet1 = PetEntity("Pet 1", 5, 10, 1, 1, None, None, None, AbilityGenerator)
        pet2 = PetEntity("Pet 2", 6, 12, 1, 1, None, None, None, AbilityGenerator)

        team.add_pet(pet1)
        team.add_pet(pet2)
        team.move_pet(0, 1)

        self.assertEqual(team.pets, [pet2, pet1])

    def test_add_pet_with_index(self):
        team = Team("Test")
        pet1 = PetEntity("Pet 1", 5, 10, 1, 1, None, None, None, AbilityGenerator)
        pet2 = PetEntity("Pet 2", 6, 12, 1, 1, None, None, None, AbilityGenerator)

        team.add_pet(pet1)
        team.add_pet(pet2, 0)

        self.assertEqual(team.pets, [pet2, pet1])


# Mock Team class to be used in tests
MockTeamA = Team("Test_A")
MockTeamB = Team("Test_B")

if __name__ == '__main__':
    unittest.main()
