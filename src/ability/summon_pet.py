from abc import abstractmethod
from src.ability.ability_abstract import AbilityBase
import src.config_utils.logger as logger
from src.pet_data_utils.enums.trigger_event import TriggerEvent
from src.action.action_utils import *

log = logger.setup_logger(__name__)
# parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
# print(parent_dir)


class Summon(AbilityBase):
    def __init__(self, owner, token, trigger_event, team_tag, n=1, level=1, attack=None, health=None):
        super().__init__(owner, trigger_event)
        self.token = token
        self.trigger_event = trigger_event
        self.team_tag = team_tag
        self.n = n
        self.level = level
        self.attack = attack
        self.health = health

    @abstractmethod
    def apply(self, pet, team, **kwargs):
        pass


class SummonSpecific(Summon):
    def apply(self, pet, team, **kwargs):
        actions = []
        if self.trigger_event == TriggerEvent.Faint:
            if self.team_tag == "Friendly":
                team_to_add_to = team
                index = team_to_add_to.pets.index(pet)
            else:
                team_to_add_to = kwargs["enemy_team"]
                index = 0

            pets_created = 0
            actions.append(generate_remove_action(self.owner, self.owner, self.owner.team))
            while pets_created < self.n:
                actions.append(generate_summon_action(None, self.token, team_to_add_to, index, is_faint_ability=True))
                pets_created += 1

            return actions
            # while pets_created < self.n:
            #     try:
            #         new_pet = create_pet(self.token)
            #         log.debug(f"{self.owner} {self.__class__.__name__} summoning {new_pet.name} to {team_to_add_to}")
            #         team_to_add_to.add_pet(new_pet, index)
            #     except KeyError:
            #         log.debug(f"Cannot create pet of type {self.token}")
            #     pets_created += 1
        else:
            print(f'{self.__class__}:{self.trigger_event} not implemented')


class SummonRandom(Summon):
    def apply(self, pet, team, **kwargs):
        pass
