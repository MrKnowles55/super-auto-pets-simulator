from src.config_utils.logger import setup_logger, log_call, log_class_init
from src.pet_data_utils.enums.trigger_event import TriggerEvent
import random

log = setup_logger(__name__)


@log_class_init(log)
class ActionHandler:
    def __init__(self):
        self.action_list = []

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @log_call(log)
    def execute_actions(self):
        actions_to_remove = []
        for action in self.action_list:
            self.execute(action)
            actions_to_remove.append(action)

        self.remove_actions(actions_to_remove)

    @log_call(log)
    def remove_actions(self, action):
        if isinstance(action, list):
            for act in action:
                self.action_list.remove(act)
        else:
            self.action_list.remove(action)

    @log_call(log)
    def clear_actions(self):
        self.action_list = []

    @log_call(log)
    def execute(self, action):
        source = action.source
        trigger_event = action.kwargs.get("trigger_event")
        # check if source is not None, and then only actually execute the action if the source pet is still alive, or if
        # the ability is a faint ability.
        if source:
            if source.is_alive or trigger_event == TriggerEvent.Faint:
                pass
            else:
                log.print("Ability not executed due to the source being dead and it not being a faint ability.")
                return
        match action.name:
            case "Damage":
                target = action.kwargs.get("target_pet")
                damage = action.kwargs.get("damage_amount")
                if target and damage and source:
                    target.apply_damage(damage, source)
                else:
                    print(
                        f"ERROR!!! Target {target}, damage {damage}, or source {source} are invalid for {action.name}")
            case "Remove":
                team = action.kwargs.get("team")
                pet = action.kwargs.get("pet_to_remove")
                team.remove_pet(pet)
            case "Summon":
                from src.pet.pet_factory import create_pet
                pet_name = action.kwargs.get("pet_to_summon")
                team = action.kwargs.get("team")
                index = action.kwargs.get("index")
                try:
                    new_pet = create_pet(pet_name)
                    team.add_pet(new_pet, index)
                except KeyError:
                    log.print(f"{pet_name} invalid pet.")
            case "Modify_Stats":
                target_pet = action.kwargs.get("target_pet")
                attack_mod = action.kwargs.get("attack_mod")
                health_mod = action.kwargs.get("health_mod")
                percentage = action.kwargs.get("percentage")
                transfer_to = action.kwargs.get("transfer_to")
                transfer_from = action.kwargs.get("transfer_from")
                if target_pet:
                    if target_pet.is_alive:
                        if percentage:
                            if transfer_to:
                                # Transfer % of stats from source to target_pet
                                attack_mod = percentage * source.attack
                                health_mod = percentage * source.health
                            elif transfer_from:
                                # Transfer % target_pet stats to source
                                attack_mod = percentage * target_pet.attack
                                health_mod = percentage * target_pet.health
                            else:
                                log.print(f"Percentage {percentage} is set but {transfer_to} and {transfer_from} are "
                                          f"invalid")
                        # Add modifiers to stats
                        target_pet.attack += attack_mod
                        target_pet.health += health_mod

                        # Set boundaries of 0 to 50 for attack, and max 50 for health.
                        target_pet.attack = min(target_pet.attack, 50)
                        target_pet.attack = max(target_pet.attack, 0)
                        target_pet.health = min(target_pet.health, 50)
                    else:
                        log.print(f"{target_pet} is fainted. Cannot modify its stats.")
                else:
                    log.print(f"Targeted pet is {target_pet}. Cannot modify its stats.")
            case _:
                print(f"Default case for ({action.name},{action.source},{action.kwargs})")
                log.print(f"Default case for ({action.name},{action.source},{action.kwargs})")

    @log_call(log)
    def add_action(self, action):
        if not action:
            return
        if isinstance(action, list):
            self.action_list.extend(action)
        else:
            self.action_list.append(action)

    @log_call(log)
    def create_actions_from_triggered_abilities(self, triggered_abilities):
        for ability_priority, ability, enemy_team, applied_damage in triggered_abilities:
            self.add_action(
                ability.apply(enemy_team=enemy_team, applied_damage=applied_damage))


@log_class_init(log)
class Action:
    def __init__(self, name, source, **kwargs):
        self.name = name
        self.source = source
        self.kwargs = kwargs

    def __repr__(self):
        attributes = ', '.join([f"{k}={repr(v)}" for k, v in vars(self).items()])
        return f"{self.__class__.__name__}({attributes})"


@log_call(log)
def collect_triggered_abilities(pet_list, trigger_event, priority, enemy_team=None, applied_damage=None):
    triggered_abilities = []
    for pet in pet_list:
        if pet.ability and pet.ability.trigger_event == trigger_event:
            if pet.is_alive:
                triggered_abilities.append((priority, pet.ability, enemy_team, applied_damage))
    return triggered_abilities


def generate_damage_action(source, trigger_event, target_pet, damage_amount):
    return generate_action("Damage", source, trigger_event=trigger_event, target_pet=target_pet,
                           damage_amount=damage_amount)


def generate_remove_action(source, trigger_event, pet_to_remove, team):
    return generate_action("Remove", source, trigger_event=trigger_event, pet_to_remove=pet_to_remove, team=team)


def generate_summon_action(source, trigger_event, pet_to_summon, team, index):
    return generate_action("Summon", source, trigger_event=trigger_event, pet_to_summon=pet_to_summon, team=team,
                           index=index)


def generate_modify_stats_action(source, trigger_event, target_pet, attack_mod, health_mod, transfer_to=False,
                                 transfer_from=False, percentage=0):
    return generate_action("Modify_Stats", source, trigger_event=trigger_event, target_pet=target_pet,
                           attack_mod=attack_mod, health_mod=health_mod, transfer_to=transfer_to,
                           transfer_from=transfer_from, percentage=percentage)


@log_call(log)
def generate_action(name, source, trigger_event, **kwargs):
    return Action(name, source, trigger_event=trigger_event, **kwargs)


action_handler = ActionHandler()
