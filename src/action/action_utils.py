import config_utils.logger as logger
import random

log = logger.setup_logger(__name__)


class ActionHandler:
    def __init__(self):
        self.action_list = []

    def execute_actions(self):
        log.info(f"Preparing to Execute {len(self.action_list)} Actions")
        # self.randomize_actions_order()
        log.info(f"Actions List: {[(action.name, action.kwargs) for action in self.action_list]}")
        actions_to_remove = []
        for action in self.action_list:
            self.execute(action)
            actions_to_remove.append(action)

        self.remove_actions(actions_to_remove)

    # def randomize_actions_order(self):
    #     log.info(f"Shuffling action_list order")
    #     random.shuffle(self.action_list)

    def remove_actions(self, action):
        if isinstance(action, list):
            for act in action:
                self.action_list.remove(act)
                log.info(f"Removing {act.name} with {act.kwargs} from action_list")
        else:
            log.info(f"Removing {action.name} action with kwargs {action.kwargs} from action_list")
            self.action_list.remove(action)

    def clear_actions(self):
        log.info("Clearing action_list")
        self.action_list = []

    def execute(self, action):
        log.info(f"Executing {action.name} with kwargs {action.kwargs}")
        match action.name:
            case "Damage":
                target = action.kwargs.get("target_pet")
                damage = action.kwargs.get("damage_amount")
                source = action.kwargs.get("source")
                if target and damage and source:
                    target.apply_damage(damage, source)
                else:
                    print(f"ERROR!!! Target {target}, damage {damage}, or source {source} are invalid for {action.name}")
            case "Remove":
                team = action.kwargs.get("team")
                pet = action.kwargs.get("pet_to_remove")
                team.remove_pet(pet)
            case "Summon":
                from pet.pet_factory import create_pet
                pet_name = action.kwargs.get("pet_to_summon")
                team = action.kwargs.get("team")
                index = action.kwargs.get("index")
                try:
                    new_pet = create_pet(pet_name)
                    team.add_pet(new_pet, index)
                except KeyError:
                    log.debug(f"{pet_name} invalid pet.")
            case _:
                print(f"Default Action for {action.name} with kwargs {action.kwargs}")
                log.info(f"Default Action for {action.name} with kwargs {action.kwargs}")

    def add(self, action):
        if isinstance(action, list):
            self.action_list.extend(action)
            for act in action:
                log.info(f"Adding {act.name} with {act.kwargs}")
        else:
            log.info(f"Adding {action.name} with {action.kwargs}")
            self.action_list.append(action)

    def create_actions_from_triggered_abilities(self, triggered_abilities):
        for ability_priority, ability, enemy_team, applied_damage in triggered_abilities:
            self.add(
                ability.apply(ability.owner, ability.owner.team, enemy_team=enemy_team, applied_damage=applied_damage))


class Action:
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs


def collect_triggered_abilities(pet_list, trigger_event, priority, enemy_team=None, applied_damage=None):
    triggered_abilities = []
    for pet in pet_list:
        if pet.ability and pet.ability.trigger_event == trigger_event:
            triggered_abilities.append((priority, pet.ability, enemy_team, applied_damage))
    return triggered_abilities


def generate_damage_action(target_pet, damage_amount, source):
    return generate_action("Damage", target_pet=target_pet, damage_amount=damage_amount, source=source)


def generate_remove_action(pet_to_remove, team):
    return generate_action("Remove", pet_to_remove=pet_to_remove, team=team)


def generate_summon_action(pet_to_summon, team, index):
    return generate_action("Summon", pet_to_summon=pet_to_summon, team=team, index=index)


def generate_action(name, **kwargs):
    log.info(f"Generating action {name} with kwargs {kwargs}")
    return Action(name, **kwargs)


action_handler = ActionHandler()

