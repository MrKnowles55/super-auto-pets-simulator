import unittest
from tests.dummy.dummy_pet import generate_dummy_pet
from tests.dummy.dummy_action import Dummy_ActionHandler
from src.team.team import Team


class TestTeam(unittest.TestCase):

    def setUp(self) -> None:
        self.action_handler = Dummy_ActionHandler()
        self.action_handler.clear_actions()
        self.test_team = Team(name="Name", handler=self.action_handler)

    def test_add_pet(self):
        pet = generate_dummy_pet(name="Pet 0")
        pet1 = generate_dummy_pet(name="Pet 1")
        pet2 = generate_dummy_pet(name="Pet 2")

        # Without Index
        self.test_team.pets_list = []
        self.test_team.add_pet(pet)

        self.assertIn(pet, self.test_team.pets_list)
        self.assertEqual(pet.team, self.test_team)
        self.assertEqual(self.test_team.length, 1)
        self.assertEqual(pet.position, 0)

        # With Index
        self.test_team.pets_list = []
        self.test_team.add_pet(pet1)
        self.test_team.add_pet(pet2)
        self.test_team.add_pet(pet, index=1)

        self.assertEqual(self.test_team.pets_list[0].name, "Pet 1")
        self.assertEqual(self.test_team.pets_list[1].name, "Pet 0")
        self.assertEqual(self.test_team.pets_list[2].name, "Pet 2")
        self.assertEqual(self.test_team.length, 3)

        # Avoid adding too many pets
        self.test_team.pets_list = []
        for _ in range(6):
            self.test_team.add_pet(pet)

        self.assertEqual(self.test_team.length, 5)

    def test_remove_pet(self):
        pet = generate_dummy_pet(name="Pet 0")
        pet1 = generate_dummy_pet(name="Pet 1")
        pet2 = generate_dummy_pet(name="Pet 2")

        # Remove from front
        self.test_team.pets_list = []
        self.test_team.pets_list.append(pet)

        self.test_team.remove_pet(pet)

        self.assertFalse(self.test_team.pets_list)
        self.assertTrue(self.action_handler.action_list)

        # Remove 1 from front with pets behind
        self.action_handler.clear_actions()
        self.test_team.pets_list = []
        self.test_team.pets_list.append(pet)
        self.test_team.pets_list.append(pet1)

        self.test_team.remove_pet(pet)

        self.assertNotIn(pet, self.test_team.pets_list)
        self.assertIn(pet1, self.test_team.pets_list)
        self.assertEqual(pet1.position, 0)

        # Remove 1 pet from middle
        self.action_handler.clear_actions()
        self.test_team.pets_list = []
        self.test_team.pets_list.append(pet)
        self.test_team.pets_list.append(pet1)
        self.test_team.pets_list.append(pet2)

        self.test_team.remove_pet(pet1)

        self.assertEqual(self.test_team.first, pet)
        self.assertEqual(pet.position, 0)
        self.assertEqual(self.test_team.pets_list[1], pet2)
        self.assertEqual(pet2.position, 1)

    def test_move_pet(self):
        pet = generate_dummy_pet(name="Pet 0")
        pet1 = generate_dummy_pet(name="Pet 1")
        pet2 = generate_dummy_pet(name="Pet 2")
        pet3 = generate_dummy_pet(name="Pet 3")
        pet4 = generate_dummy_pet(name="Pet 4")

        # Move empty space
        self.test_team.pets_list = []
        self.test_team.pets_list.append(pet)
        pet.position = 0

        self.test_team.move_pet(4, 0)

        self.assertEqual(self.test_team.first, pet)
        self.assertEqual(self.test_team.length, 1)

        # Move in place, 1 pet
        self.test_team.pets_list = []
        self.test_team.pets_list.append(pet)
        pet.position = 0

        self.test_team.move_pet(0, 0)

        self.assertEqual(self.test_team.first, pet)
        self.assertEqual(pet.position, 0)

        # Move in place, full team
        self.test_team.pets_list = []
        self.test_team.pets_list.append(pet)
        self.test_team.pets_list.append(pet1)
        self.test_team.pets_list.append(pet2)
        self.test_team.pets_list.append(pet3)
        self.test_team.pets_list.append(pet4)
        pet.position = 0
        pet1.position = 1
        pet2.position = 2
        pet3.position = 3
        pet4.position = 4

        self.test_team.move_pet(0, 0)

        self.assertEqual(self.test_team.first, pet)
        self.assertEqual(pet.position, 0)
        self.assertEqual(self.test_team.pets_list[1], pet1)
        self.assertEqual(pet1.position, 1)
        self.assertEqual(self.test_team.pets_list[2], pet2)
        self.assertEqual(pet2.position, 2)
        self.assertEqual(self.test_team.pets_list[3], pet3)
        self.assertEqual(pet3.position, 3)
        self.assertEqual(self.test_team.pets_list[4], pet4)
        self.assertEqual(pet4.position, 4)

        # Move to index > team length
        self.test_team.pets_list = []
        self.test_team.pets_list.append(pet)
        pet.position = 0

        self.test_team.move_pet(0, 4)

        self.assertEqual(self.test_team.first, pet)
        self.assertEqual(pet.position, 0)

        # Move 0 to 1 with 2 pets
        self.test_team.pets_list = []
        self.test_team.pets_list.append(pet)
        self.test_team.pets_list.append(pet1)
        pet.position = 0
        pet1.position = 1

        self.test_team.move_pet(0, 1)

        self.assertEqual(self.test_team.first, pet1)
        self.assertEqual(pet1.position, 0)
        self.assertEqual(self.test_team.pets_list[1], pet)
        self.assertEqual(pet.position, 1)
        self.assertEqual(self.test_team.length, 2)

    def test_update_positions(self):
        pet = generate_dummy_pet(name="Pet 0")
        pet1 = generate_dummy_pet(name="Pet 1")
        pet2 = generate_dummy_pet(name="Pet 2")
        pet3 = generate_dummy_pet(name="Pet 3")
        pet4 = generate_dummy_pet(name="Pet 4")
        self.test_team.pets_list = []
        self.test_team.pets_list.append(pet)
        self.test_team.pets_list.append(pet1)
        self.test_team.pets_list.append(pet2)
        self.test_team.pets_list.append(pet3)
        self.test_team.pets_list.append(pet4)
        pet.position = 4
        pet1.position = 2
        pet2.position = 3
        pet3.position = 0
        pet4.position = 1

        self.test_team.update_positions()

        self.assertEqual(pet.position, 0)
        self.assertEqual(pet1.position, 1)
        self.assertEqual(pet2.position, 2)
        self.assertEqual(pet3.position, 3)
        self.assertEqual(pet4.position, 4)


if __name__ == '__main__':
    unittest.main()
