from src.action.action_utils import action_handler, collect_triggered_abilities
from src.pet_data_utils.enums.trigger_event import TriggerEvent
from config_utils.logger import setup_logger, log_call

# directory = os.path.dirname(os.path.abspath(__file__))
log = setup_logger(__name__)


def get_battle_string(team1, team2, prefix='', format_buffer=80, name_length=8):
    """
    Create a formatted battle string representing the current state of both teams.

    :param team1: The first team of pets.
    :param team2: The second team of pets.
    :param prefix: A string prefix to be added at the beginning of the output string.
    :param format_buffer: The width of each team string in the formatted output.
    :param name_length: The maximum length of pet names in the output.
    :return: A formatted string representing the current state of both teams.
    """
    team1_pets_str = ['_'] * 5
    team2_pets_str = ['_'] * 5
    for i, pet in enumerate(team1.pets):
        team1_pets_str[i] = f"{pet.name[:name_length]}({pet.attack}/{pet.health})"
    for i, pet in enumerate(team2.pets):
        team2_pets_str[i] = f"{pet.name[:name_length]}({pet.attack}/{pet.health})"
    team1_pets_str = ', '.join(reversed(team1_pets_str))
    team2_pets_str = ', '.join(team2_pets_str)
    len1 = len(team1_pets_str)
    len2 = len(team2_pets_str)
    max_len = max(len1, len2)
    return f"{prefix} {team1_pets_str:>{format_buffer}}     VS     {team2_pets_str:<{format_buffer}}"


def get_pet_list(team1, team2):
    return team1.pets + team2.pets


def start_of_battle(team1, team2, pet_list, verbose=False):
    log.print(get_battle_string(team1, team2, "Begin start_of_battle(): "))
    actions = []
    priority_dict = prioritize_pets(pet_list)
    priorities = sorted(priority_dict.keys(), reverse=True)
    log.print(f"start_of_battle priorities list {priorities}")

    # Initialize applied damage dictionary
    applied_damage = {}

    for priority in priorities:
        pets_with_same_priority = priority_dict[priority]
        log.print(f"start_of_battle pets in priority {priority} : {pets_with_same_priority}")

        # Collect abilities that should trigger for StartOfBattle event
        triggered_abilities = []
        for pet in pets_with_same_priority:
            if pet.team == team1:
                triggered_abilities += collect_triggered_abilities([pet], TriggerEvent.StartOfBattle, priority,
                                                                   enemy_team=team2, applied_damage=applied_damage)
            else:
                triggered_abilities += collect_triggered_abilities([pet], TriggerEvent.StartOfBattle, priority,
                                                                   enemy_team=team1, applied_damage=applied_damage)
        log.print(f"start_of_battle triggered_abilities {triggered_abilities}")
        # Execute the collected abilities
        action_handler.create_actions_from_triggered_abilities(triggered_abilities)
        action_handler.execute_actions()

    if verbose:
        print(get_battle_string(team1, team2, prefix="Start of Battle"))
    log.print(get_battle_string(team1, team2, "End start_of_battle(): "))


def fight_loop(team1, team2, verbose=False):
    # Fight Loop
    log.print(get_battle_string(team1, team2, "Begin fight_loop(): "))
    round = 0
    while team1.pets and team2.pets:
        action_handler.execute_actions()
        pet1 = team1.pets[0]
        pet2 = team2.pets[0]

        round += 1

        log.print(get_battle_string(team1, team2, prefix=f'Before Attack :'))

        pet1.before_attack()
        pet2.before_attack()

        log.print(get_battle_string(team1, team2, prefix=f'Attack Round ({round}):'))

        pet1.attack_pet(pet2)

        log.print(get_battle_string(team1, team2, prefix=f'After Attack :'))
        if verbose:
            print(get_battle_string(team1, team2, prefix=f'After Attack :'))

    if verbose:
        if not team1.pets:
            print("Player Loses! =(")
        if not team2.pets:
            print("Player Wins!!! =D")
        if not team1.pets and not team2.pets:
            print("It's a tie. =/")
    log.print(get_battle_string(team1, team2, "End fight_loop(): "))


def end_of_battle(team1, team2, verbose=False):
    # End of Battle
    log.print(get_battle_string(team1, team2, prefix=f'End fight() :'))
    return [int(bool(team1.pets)), int(bool(team2.pets))]

@log_call(log)
def fight(team1, team2, verbose=False):
    """
    Simulate a battle between two teams of pets.

    :param team1: The first team of pets.
    :param team2: The second team of pets.
    :param verbose: Whether to print battle information.
    :return: A list containing the result of the battle for each team (1 if the team won, 0 otherwise).
    """
    log.print(get_battle_string(team1, team2, prefix='Begin fight() :'))

    if verbose:

        print("\n")
        print(get_battle_string(team1, team2, prefix='Initial Board :'))

    # Start of Battle
    pet_list = get_pet_list(team1, team2)

    priority_dict = prioritize_pets(pet_list)

    start_of_battle(team1, team2, pet_list, verbose)
    fight_loop(team1, team2, verbose)

    return end_of_battle(team1, team2, verbose)


def prioritize_pets(pet_list, priority_key=lambda x: x.attack):
    """
    Create a dictionary of pets prioritized by a given attribute.

    :param pet_list: A list of pets to prioritize.
    :param priority_key: A function that takes a pet and returns a value to prioritize the pet by.
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
