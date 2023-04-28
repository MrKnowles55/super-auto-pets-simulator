import src.logger as logger

log = logger.setup_logger(__name__)


class ActionHandler:
    def __init__(self):
        self.action_list = []

    def execute_actions(self):
        log.info(f"Preparing to Execute {len(self.action_list)} Actions")
        actions_to_remove = []
        for action in self.action_list:
            self.execute(action)
            actions_to_remove.append(action)

        for action in actions_to_remove:
            self.remove_actions(action)

    def remove_actions(self, action):
        if isinstance(action, list):
            for act in action:
                self.action_list.remove(act)
                log.info(f"Removing {act.name} with {act.kwargs} from action_list")
        else:
            log.info(f"Removing {action.name} with kwargs {action.kwargs} from action_list")
            self.action_list.remove(action)

    def clear_actions(self):
        log.info("Clearing action_list")
        self.action_list = []

    def execute(self, action):
        log.info(f"Executing {action.name} with kwargs {action.kwargs}")
        print(action.name, action.kwargs)
        match action.name:
            case "Damage":
                target = action.kwargs.get("target_pet")
                damage = action.kwargs.get("damage_amount")
                source = action.kwargs.get("source")
                if target and damage and source:
                    target.apply_damage(damage, source)
                else:
                    print(f"ERROR!!! Target {target}, damage {damage}, or source {source} are invalid for {action.name}")

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
    return Action("Damage", target_pet=target_pet, damage_amount=damage_amount, source=source)


action_handler = ActionHandler()

