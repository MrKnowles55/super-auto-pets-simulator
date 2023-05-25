from abc import abstractmethod
from data.old.depreciated.ability.ability_abstract import AbilityBase
from data.old.depreciated.action_utils import *

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
                index = team_to_add_to.pets_list.index(self.owner)
            else:
                team_to_add_to = kwargs["enemy_team"]
                index = 0

            pets_created = 0
            actions.append(generate_remove_action(source=self.owner, trigger_event=self.trigger_event, pet_to_remove=self.owner, team=self.owner.team))
            while pets_created < self.n:
                actions.append(generate_summon_action(source=self.owner, trigger_event=self.trigger_event, pet_to_summon=self.token, team=team_to_add_to, index=index))
                pets_created += 1

            return actions

        else:
            print(f'{self.__class__}:{self.trigger_event} not implemented')


@log_class_init(log)
class SummonRandom(Summon):
    @log_call(log)
    def apply(self, **kwargs):
        pass
