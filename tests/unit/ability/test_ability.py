import unittest

from src.ability.ability_abstract import AbilityBase, No_Ability
from src.pet_data_utils.enums.trigger_event import TriggerEvent

from tests.dummy.dummy_pet import DummyPet


class Fake_Ability(AbilityBase):
    def apply(self, **kwargs):
        return self.trigger_event


class TestAbility(unittest.TestCase):
    def setUp(self):
        self.ability_none = No_Ability(owner=None)
        self.ability_fake = Fake_Ability(owner=None, trigger_event=None)

    def test_init(self):
        # No Ability
        self.assertFalse(self.ability_none.owner)
        self.assertFalse(self.ability_none.trigger_event)

        # Fake ability
        fake_pet = DummyPet()
        new_ability = Fake_Ability(owner=fake_pet, trigger_event=TriggerEvent.Hurt)

        self.assertEqual(new_ability.owner, fake_pet)
        self.assertEqual(new_ability.trigger_event, TriggerEvent.Hurt)

    def test_apply(self):
        # No ability
        self.assertFalse(self.ability_none.apply())

        # Fake Ability
        self.ability_fake.trigger_event = TriggerEvent.Sell
        self.assertEqual(self.ability_fake.apply(), TriggerEvent.Sell)

    def test_trigger(self):
        for event in TriggerEvent:
            # No ability
            self.assertFalse(self.ability_none.trigger(event))

            # Fake Ability
            self.ability_fake.trigger_event = event
            self.assertEqual(self.ability_fake.trigger(event), event)


if __name__ == '__main__':
    unittest.main()
