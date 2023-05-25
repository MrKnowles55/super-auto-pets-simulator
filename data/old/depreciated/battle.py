from data.old.depreciated.action_utils import action_handler
from src.config_utils.logger import setup_logger, log_call

# directory = os.path.dirname(os.path.abspath(__file__))
log = setup_logger(__name__)


def get_battle_string(team1, team2, prefix='', prefix_buffer=10,format_buffer=80, name_length=8):
    """
    Create a formatted battle string representing the current state of both teams.

    :param team1: The first team_utils of pets.
    :param team2: The second team_utils of pets.
    :param prefix: A string prefix to be added at the beginning of the output string.
    :param format_buffer: The width of each team_utils string in the formatted output.
    :param name_length: The maximum length of pet_utils names in the output.
    :return: A formatted string representing the current state of both teams.
    """
    team1_pets_str = ['_'] * 5
    team2_pets_str = ['_'] * 5
    for i, pet in enumerate(team1.pets_list):
        team1_pets_str[i] = pet.__str__()
    for i, pet in enumerate(team2.pets_list):
        team2_pets_str[i] = pet.__str__()
    team1_pets_str = ', '.join(reversed(team1_pets_str))
    team2_pets_str = ', '.join(team2_pets_str)
    len1 = len(team1_pets_str)
    len2 = len(team2_pets_str)
    max_len = max(len1, len2)
    return f"{prefix:{prefix_buffer}} {team1_pets_str:>{format_buffer}}     VS     {team2_pets_str:<{format_buffer}}"


def get_pet_list(team1, team2):
    return team1.pets_list + team2.pets_list


# def old_start_of_battle(team1, team2, pet_list, verbose=False):
#     log.print(get_battle_string(team1, team2, "Begin start_of_battle(): "))
#     if verbose:
#         print(get_battle_string(team1, team2, f"Begin: "))
#     actions = []
#     priority_dict = prioritize_pets(pet_list)
#     priorities = sorted(priority_dict.keys(), reverse=True)
#     log.print(f"start_of_battle priorities list {priorities}")
#
#     # Initialize applied damage dictionary
#     applied_damage = {}
#
#     for priority in priorities:
#         pets_with_same_priority = priority_dict[priority]
#         log.print(f"start_of_battle pets in priority {priority} : {pets_with_same_priority}")
#
#         # Collect abilities that should trigger for StartOfBattle event
#         triggered_abilities = []
#         for pet_utils in pets_with_same_priority:
#             if pet_utils.team_utils == team1:
#                 triggered_abilities += collect_triggered_abilities([pet_utils], TriggerEvent.StartOfBattle, priority,
#                                                                    enemy_team=team2, applied_damage=applied_damage)
#             else:
#                 triggered_abilities += collect_triggered_abilities([pet_utils], TriggerEvent.StartOfBattle, priority,
#                                                                    enemy_team=team1, applied_damage=applied_damage)
#         log.print(f"start_of_battle triggered_abilities {triggered_abilities}")
#         # Execute the collected abilities
#         action_handler.create_actions_from_triggered_abilities(triggered_abilities)
#         action_handler.execute_actions()
#
#     log.print(get_battle_string(team1, team2, "End start_of_battle(): "))


@log_call(log)
def start_of_battle(team1, team2, verbose=False):
    if verbose:
        print(get_battle_string(team1, team2, f"Start of Battle: "))
    action_handler.execute_actions()
    for pet in team1.pets_list:
        pet.start_of_battle(team2)
    for pet in team2.pets_list:
        pet.start_of_battle(team1)


@log_call(log)
def perform_round(team1, team2, verbose=False):
    action_handler.execute_actions()

    pet1 = team1.first
    pet2 = team2.first

    before_attack(pet1, pet2)

    attack(pet1, pet2)

    after_attack(pet1, pet2)


@log_call(log)
def before_attack(pet1, pet2, verbose=False):
    action_handler.execute_actions()
    pet1.before_attack()
    pet2.before_attack()


@log_call(log)
def attack(pet1, pet2, verbose=False):
    action_handler.execute_actions()

    pet1.attack_pet(pet2)


@log_call(log)
def after_attack(pet1, pet2, verbose=False):
    action_handler.execute_actions()

    pet1.after_attack()
    pet2.after_attack()

    action_handler.execute_actions()


@log_call(log)
def is_battle_over(team1, team2):
    return not (team1.pets_list and team2.pets_list)


@log_call(log)
def fight_loop(team1, team2, loop_limit=1000, verbose=False):
    round = 0
    while not is_battle_over(team1, team2):
        action_handler.execute_actions()
        round += 1
        if verbose:
            print(get_battle_string(team1, team2, f"Round {round}: "))
        perform_round(team1, team2)

        if round >= loop_limit:
            break
    return round


@log_call(log)
def end_of_battle(team1, team2, verbose=False):
    # End of Battle
    if verbose:
        print(get_battle_string(team1, team2, f"End: "))
    log.print(get_battle_string(team1, team2, prefix=f'End fight() :'))
    return [int(bool(team1.pets_list)), int(bool(team2.pets_list))]


@log_call(log)
def fight(team1, team2, verbose=False):
    """
    Simulate a battle between two teams of pets.

    :param team1: The first team_utils of pets.
    :param team2: The second team_utils of pets.
    :param verbose: Whether to print battle information.
    :return: A list containing the result of the battle for each team_utils (1 if the team_utils won, 0 otherwise).
    """

    # Start of Battle
    # pet_list = get_pet_list(team1, team2)

    start_of_battle(team1, team2, verbose)
    rounds = fight_loop(team1, team2, verbose=verbose)

    return end_of_battle(team1, team2, verbose)


def prioritize_pets(pet_list, priority_key=lambda x: x.attack):
    """
    Create a dictionary of pets prioritized by a given attribute.

    :param pet_list: A list of pets to prioritize.
    :param priority_key: A function that takes a pet_utils and returns a value to prioritize the pet_utils by.
    :return: A dictionary where keys are priorities and values are lists of pets with that priority.
    """
    sorted_pets = sorted(pet_list, key=priority_key, reverse=True)

    priority_dict = {}
    for pet in sorted_pets:
        priority = priority_key(pet)
        if priority not in priority_dict:
            priority_dict[priority] = []
        priority_dict[priority].append(pet)

    return priority_dict
