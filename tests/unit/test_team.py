import unittest
from unittest.mock import MagicMock, patch

from src.team_utils.team import Team

from src.data_utils.enums.trigger_event import TriggerEvent
from src.data_utils.enums.trigger_by_kind import TriggerByKind
from src.data_utils.enums.effect_target_kind import EffectTargetKind
from src.data_utils.enums.effect_kind import EffectKind


class TestTeam(unittest.TestCase):
    def setUp(self) -> None:
        self.team = Team("Test")
        self.pets = {}
        for _ in range(6):
            _ += 1
            new_pet = MagicMock()
            new_pet.name = f"Pet_{_}"
            new_pet.position = -1

            def make_update_position_side_effect(pet):
                def update_position_side_effect(new_position):
                    pet.position = new_position
                return update_position_side_effect

            new_pet.update_position.side_effect = make_update_position_side_effect(new_pet)
            self.pets[_] = new_pet
        print("\n")

    def test_add_pet_5_max(self):

        # Attempt to add 6 pets, should only receive the first 5
        # Ensure pet is added, its team and position are updated.

        self.assertEqual(self.team.length, 0)
        for key, pet in self.pets.items():
            self.team.add_pet(pet)

            if key <= 5:
                self.assertEqual(self.team.length, key)
                self.assertEqual(self.team.pets_list[key-1], pet)
                self.assertEqual(self.team.pets_list[key - 1].team, self.team)
                self.assertEqual(self.team.pets_list[key - 1].update_position.call_count, 1)
            elif key > 5:
                self.assertEqual(self.team.length, 5)
            else:
                raise ValueError

    def test_add_pet_index(self):

        # Ensure adding by index still shrinks list to minimum size
        for _ in range(5):
            self.team.pets_list = []
            self.team.add_pet(self.pets[1], _)
            # Check order and positions
            self.assertEqual(self.team.pets_list, [self.pets[1]])
            self.assertEqual(self.pets[1].position, 0)

        # Ensure adding to full list does nothing
        self.team.pets_list = []
        for _ in range(1, 6):
            self.team.add_pet(self.pets[_])

        self.team.add_pet(self.pets[6])

        self.assertEqual(self.team.pets_list, [self.pets[1], self.pets[2], self.pets[3], self.pets[4], self.pets[5]])
        for i, pet in enumerate(self.team.pets_list):
            self.assertEqual(pet.position, i)

        # Test with 4 pets in team
        self.team.pets_list = []
        for _ in range(1, 5):
            self.team.add_pet(self.pets[_])

        # Add to the middle
        self.team.add_pet(self.pets[5], index=2)

        self.assertEqual(self.team.pets_list, [self.pets[1], self.pets[2], self.pets[5], self.pets[3], self.pets[4]])
        for i, pet in enumerate(self.team.pets_list):
            self.assertEqual(pet.position, i)

    # def test_remove_pet(self): #TODO Fix
    #     action_handler = MagicMock()
    #     action_handler.create_action = MagicMock()
    #     self.team.action_handler = action_handler
    #
    #     self.team.pets_list = [self.pets[1]]
    #
    #     self.team.remove_pet(self.pets[1])
    #
    #     self.team.action_handler.create_action.assert_called_with(self.pets[1], None, None)

    def test_move_pet(self):
        # Moving nothing
        self.team.move_pet(0, 1)
        self.assertFalse(self.team.length)

        # Moving 1 pet in len 1 team
        self.team.add_pet(self.pets[1])

        self.team.move_pet(0, 4)

        self.assertEqual(self.team.pets_list, [self.pets[1]])
        self.assertEqual(self.pets[1].position, 0)

        # Indices not between 0 and 4
        self.team.move_pet(-1, 1)
        self.team.move_pet(1, -1)
        self.team.move_pet(9, 1)
        self.team.move_pet(1, 9)

        self.assertEqual(self.team.pets_list, [self.pets[1]])
        self.assertEqual(self.pets[1].position, 0)

        # Move pet into occupied space
        self.team.add_pet(self.pets[2])

        self.team.move_pet(0, 1)

        self.assertEqual(self.team.pets_list, [self.pets[2], self.pets[1]])
        self.assertEqual(self.pets[2].position, 0)
        self.assertEqual(self.pets[1].position, 1)

        # Move pet with full team
        self.team.add_pet(self.pets[3])
        self.team.add_pet(self.pets[4])
        self.team.add_pet(self.pets[5])

        self.team.move_pet(0, 4)

        self.assertEqual(self.team.pets_list, [self.pets[1], self.pets[3], self.pets[4], self.pets[5], self.pets[2]])

    def test_update_position(self):
        # No pets
        self.team.update_positions()

        # With pets
        self.team.pets_list = [self.pets[1],self.pets[2],self.pets[3],self.pets[4], self.pets[5]]

        self.team.update_positions()

        for key, pet in self.pets.items():
            if pet in self.team.pets_list:
                self.assertEqual(pet.position, key-1)

