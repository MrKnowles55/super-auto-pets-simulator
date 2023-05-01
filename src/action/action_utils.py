from config_utils.logger import setup_logger, log_call, log_class_init
import random

log = setup_logger(__name__)


@log_class_init(log)
class ActionHandler:
    def __init__(self):
        self.action_list = []

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
        is_faint_ability = action.kwargs.get("is_faint_ability", False)
        # check if source is not None, and then only actually execute the action if the source pet is still alive, or if
        # the ability is a faint ability.
        if source:
            if source.is_alive or is_faint_ability:
                pass
            else:
                return
        match action.name:
            case "Damage":
                target = action.kwargs.get("target_pet")
                damage = action.kwargs.get("damage_amount")
                if target and damage and source:
                    target.apply_damage(damage, source)
                else:
                    print(f"ERROR!!! Target {target}, damage {damage}, or source {source} are invalid for {action.name}")
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
                    log.debug(f"{pet_name} invalid pet.")
            case _:
                print(f"Default case for ({action.name},{action.source},{action.kwargs})")
                log.info(f"Default case for ({action.name},{action.source},{action.kwargs})")

    @log_call(log)
    def add(self, action):
        if not action:
            return
        if isinstance(action, list):
            self.action_list.extend(action)
        else:
            self.action_list.append(action)

    @log_call(log)
    def create_actions_from_triggered_abilities(self, triggered_abilities):
        for ability_priority, ability, enemy_team, applied_damage in triggered_abilities:
            self.add(
                ability.apply(enemy_team=enemy_team, applied_damage=applied_damage))


@log_class_init(log)
class Action:
    def __init__(self, name, source, **kwargs):
        self.name = name
        self.source = source
        self.kwargs = kwargs


@log_call(log)
def collect_triggered_abilities(pet_list, trigger_event, priority, enemy_team=None, applied_damage=None):
    triggered_abilities = []
    for pet in pet_list:
        if pet.ability and pet.ability.trigger_event == trigger_event:
            if pet.is_alive:
                triggered_abilities.append((priority, pet.ability, enemy_team, applied_damage))
    return triggered_abilities


def generate_damage_action(source, target_pet, damage_amount, is_faint_ability=False):
    return generate_action("Damage", source, target_pet=target_pet, damage_amount=damage_amount,
                           is_faint_ability=is_faint_ability)


def generate_remove_action(source, pet_to_remove, team, is_faint_ability=False):
    return generate_action("Remove", source, pet_to_remove=pet_to_remove, team=team,
                           is_faint_ability=is_faint_ability)


def generate_summon_action(source, pet_to_summon, team, index, is_faint_ability=False):
    return generate_action("Summon", source, pet_to_summon=pet_to_summon, team=team, index=index,
                           is_faint_ability=is_faint_ability)


@log_call(log)
def generate_action(name, source, **kwargs):
    return Action(name, source, **kwargs)


action_handler = ActionHandler()

