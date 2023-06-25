import json
import os

from src.pet_utils.pet import enum_to_string, string_to_enum
from src.pet_utils.target import Targeter
from src.team_utils.team import Team
from src.data_utils.ability_enums import EffectKind, EffectTargetKind, TriggerByKind, TriggerEvent


directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, "../data/perk_data.json")


class Food:
    def __init__(self, name, **kwargs):
        self.name = name.title()

        # Default Parameters
        self.cost = 3

        # Base parameters
        template = self._get_data()["foods"]["food-"+self.id]
        for key, value in template.items():
            if key != "id":
                setattr(self, key, value)

        # Team Parameters
        self.team = None
        self.position = -1

        # set additional attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def target_handler(self):
        try:
            return self.team.action_handler.target_handler
        except AttributeError:
            return Targeter()

    @property
    def id(self):
        return self.name.lower().replace(" ", "-")

    @property
    def description(self):
        return self.__getattribute__('ability').get('description')

    @property
    def effect(self):
        return string_to_enum(self.__getattribute__("ability").get("effect", {}).get("kind"), EffectKind)

    @property
    def target(self):
        return string_to_enum(self.__getattribute__("ability").get("effect", {}).get("target", {}).get("kind"), EffectTargetKind)

    @property
    def effect_kwargs(self):
        temp = {key:value for key, value in self.__getattribute__("ability").get("effect",{}).items() if key not in ['target']}
        return temp

    @staticmethod
    def _get_data(source=filename):
        with open(source) as f:
            return json.load(f)

    def _get_target(self, **kwargs):
        return getattr(self.target_handler, 'target_' + enum_to_string(kwargs.get("target")))(self, **kwargs)

    def buy(self):
        print(f"{self.name} bought for {self.cost} Gold. {self.description} Target {self.target}")
        target = self._get_target(target=self.target)
        print(target, self.effect)
        getattr(target[0], self.effect.name)(target=EffectTargetKind.Self, **self.effect_kwargs)


if __name__ == "__main__":
    foo = Food("apple")
    for k, v in foo.__dict__.items():
        print(k, v)