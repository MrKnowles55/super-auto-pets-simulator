from abc import abstractmethod
from src.ability.ability_abstract import AbilityBase
from src.config_utils.logger import setup_logger, log_call, log_class_init
from src.pet_data_utils.enums.trigger_event import TriggerEvent
from src.action.action_utils import *

log = setup_logger(__name__)
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

    @log_call(log)
    @abstractmethod
    def apply(self, **kwargs):
        pass


@log_class_init(log)
class SummonSpecific(Summon):
    @log_call(log)
    def apply(self, **kwargs):
        actions = []
        if self.trigger_event == TriggerEvent.Faint:
            if self.team_tag == "Friendly":
                team_to_add_to = self.owner.team
                index = team_to_add_to.pets.index(self.owner)
            else:
                team_to_add_to = kwargs["enemy_team"]
                index = 0

            pets_created = 0
            actions.append(generate_remove_action(self.owner, self.owner, self.owner.team))
            while pets_created < self.n:
                actions.append(generate_summon_action(None, self.token, team_to_add_to, index, is_faint_ability=True))
                pets_created += 1

            return actions

        else:
            print(f'{self.__class__}:{self.trigger_event} not implemented')


@log_class_init(log)
class SummonRandom(Summon):
    @log_call(log)
    def apply(self, **kwargs):
        pass
