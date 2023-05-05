import unittest
from src.pet.pet_entity import PetEntity
from src.ability.ability_generator import AbilityGenerator
from src.ability.ability_abstract import AbilityBase, No_Ability
from src.team.team import Team
from src.pet_data_utils.enums.trigger_event import TriggerEvent


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


class Test_AbilityBase:
    def __init__(self, owner, trigger_event=None):
        self.owner = owner
        self.trigger_event = trigger_event

    def apply(self, **kwargs):
        if self.trigger_event:
            return self.trigger_event.name, kwargs

        return "None", kwargs

    def trigger(self, event, **kwargs):
        if event == self.trigger_event:
            return self.apply(**kwargs)


class Test_NoAbility(Test_AbilityBase):
    def __init__(self, owner):
        super().__init__(owner)


class Test_HurtAbility(Test_AbilityBase):
    def __init__(self, owner, trigger_event=TriggerEvent.Hurt):
        super().__init__(owner, trigger_event)


def generate_test_ability(owner, trigger_event=None):
    trigger_event_dict = {item.name.lower(): item for item in TriggerEvent}

    if trigger_event and trigger_event.lower() in trigger_event_dict:
        trigger_event = trigger_event_dict[trigger_event.lower()]
    else:
        trigger_event = None

    return Test_AbilityBase(owner, trigger_event)


if __name__ == '__main__':
    unittest.main()
