from src.config_utils.logger import setup_logger, log_call, log_class_init
from src.pet_data_utils.enums.trigger_event import TriggerEvent
import random

log = setup_logger(__name__)


@log_class_init(log)
class ActionHandler:
    def __init__(self):
        self.action_list = []
        self.priority_dict = {}
        self.team_action_list = []

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @log_call(log)
    @log_call(log)
    def execute_actions(self):
        while self.action_list:
            self.priority_dict = self.prioritize_actions()
            priorities = sorted(list(self.priority_dict.keys()), reverse=True)

            for priority in priorities:
                # Execute pet actions with the current priority
                for action in self.priority_dict[priority]:
                    self.execute(action)
                    self.remove_actions(action)

                # Execute team actions after each priority
                for team_action in self.team_action_list:
                    self.execute(team_action)
                    self.remove_actions(team_action)

                self.team_action_list = []  # Clear team_action_list after executing team actions for the current priority

            # for priority in priorities:
            #     log.print(f"Inside Team {self.team_action_list}")
            #     for action in self.priority_dict[priority]:
            #         self.execute(action)
            #     for action in self.team_action_list:
            #         self.execute(action)
            # self.clear_actions()
        #     actions_to_remove.append(action)
        #
        # self.remove_actions(actions_to_remove)

    @log_call(log)
    def prioritize_actions(self):
        from src.team.team import Team
        actions_to_prioritize = [x for x in self.action_list if x is not None and x.source is not None and
                                 not isinstance(x.source, Team)]
        unique_priorities = set(x.source.attack for x in actions_to_prioritize)
        priority_dict = {priority: [x for x in actions_to_prioritize if x.source.attack == priority] for priority in
                         unique_priorities}

        # Get team actions
        team_actions = [x for x in self.action_list if isinstance(x.source, Team)]
        self.team_action_list.extend(team_actions)

        # Get the top priority
        if unique_priorities:
            top_priority = max(unique_priorities)
        else:
            top_priority = 0.5

        # Insert team actions just below the top priority
        priority_dict[top_priority - 0.5] = team_actions

        # Sort the priority_dict by priority in descending order
        sorted_priority_dict = dict(sorted(priority_dict.items(), key=lambda item: item[0], reverse=True))

        return sorted_priority_dict

    @log_call(log)
    def remove_actions(self, action):
        if isinstance(action, list):
            for act in action:
                self.action_list.remove(act)
        else:
            try:
                self.action_list.remove(action)
            except ValueError:
                pass

    @log_call(log)
    def clear_actions(self):
        self.action_list = []

    @log_call(log)
    def retarget_action(self, action, **kwargs):
        source = action.source
        new_actions = source.ability.apply(**kwargs)
        for act in new_actions:
            if act.name == action.name:
                return act

    @log_call(log)
    def execute(self, action, retarget_flag=False):
        from src.team.team import player_team, opponent_team
        log.print(f"{list(reversed(player_team.pets_list))} vs {opponent_team.pets_list}")
        source = action.source
        trigger_event = action.kwargs.get("trigger_event")
        # check if source is not None, and then only actually execute the action if the source pet is still alive, or if
        # the ability is a faint ability. Try method to capture is_alive attribute for pets, but bypass if
        # source is not a pet.
        try:
            source_alive_flag = source.is_alive
        except AttributeError:
            source_alive_flag = True

        if source:
            if source_alive_flag or trigger_event == TriggerEvent.Faint:
                pass
            else:
                log.print("Ability not executed due to the source being dead and it not being a faint ability.")
                return
        match action.name:
            case "Damage":
                target = action.kwargs.get("target_pet")
                damage = action.kwargs.get("damage_amount")
                if target and damage and source:
                    if target.is_alive:
                        target.apply_damage(damage, source)
                    else:
                        from src.team.team import player_team, opponent_team
                        enemy_team = opponent_team if action.source.team == player_team else player_team
                        new_action = self.retarget_action(action, enemy_team=enemy_team)
                        self.execute(new_action, retarget_flag=True)
                else:
                    print(
                        f"ERROR!!! Target {target}, damage {damage}, or source {source} are invalid for {action.name}")
            case "Remove":
                team = action.kwargs.get("team")
                pet = action.kwargs.get("pet_to_remove")
                try:
                    team.pets_list.remove(pet)
                except ValueError:
                    pass
                team.update_positions()
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
                exclude = action.kwargs.get("exclude")
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

                        log.print(f"{source} modified {target_pet} from {source.team.pets_list}")
                    else:
                        if not retarget_flag:
                            log.print(f"{target_pet} is fainted. Retargeting.")
                            index = action.kwargs.get("index")
                            if index is not None:
                                if exclude is not None:
                                    new_action = self.retarget_action(action, index=index, exclude=exclude)
                                else:
                                    new_action = self.retarget_action(action, index=index)
                            else:
                                new_action = self.retarget_action(action)
                            if new_action:
                                self.execute(new_action, retarget_flag=True)
                            else:
                                log.print(f"{target_pet} is fainted. No other Targets available.")
                        else:
                            log.print(f"Retarget failed.")
                else:
                    log.print(f"Targeted pet is {target_pet}. Cannot modify its stats.")
            case "Fill":
                if source:
                    source.fill()
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
                                 transfer_from=False, percentage=0, **kwargs):
    return generate_action("Modify_Stats", source, trigger_event=trigger_event, target_pet=target_pet,
                           attack_mod=attack_mod, health_mod=health_mod, transfer_to=transfer_to,
                           transfer_from=transfer_from, percentage=percentage, **kwargs)


def generate_fill_action(source, trigger_event=None):
    return generate_action("Fill", source, trigger_event=trigger_event)


@log_call(log)
def generate_action(name, source, trigger_event, **kwargs):
    return Action(name, source, trigger_event=trigger_event, **kwargs)


action_handler = ActionHandler()
