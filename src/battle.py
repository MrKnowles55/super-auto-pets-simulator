from pet import prioritize_pets
import logger

log = logger.setup_logger(__name__)


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
    return f"{prefix:<20} {team1_pets_str:>{format_buffer}}     VS     {team2_pets_str:<{format_buffer}}"


def get_pet_list(team1, team2):
    return team1.pets + team2.pets


def fight(team1, team2, verbose):
    """
    Simulate a battle between two teams of pets.

    :param team1: The first team of pets.
    :param team2: The second team of pets.
    :param verbose: Whether to print battle information.
    :return: A list containing the result of the battle for each team (1 if the team won, 0 otherwise).
    """
    log.debug("Starting Fight")
    log.debug(get_battle_string(team1, team2, prefix='Start of Battle :'))

    if verbose:

        print("\n")
        print(get_battle_string(team1, team2, prefix='Start of Battle :'))

    # Start of Battle
    pet_list = get_pet_list(team1, team2)

    priority_dict = prioritize_pets(pet_list)

    for priority in sorted(priority_dict.keys(), reverse=True):
        pets_with_same_priority = priority_dict[priority]

        for pet in pets_with_same_priority:
            if pet.team == team1:
                pet.start_of_battle(enemy_team=team2)
            else:
                pet.start_of_battle(enemy_team=team1)

    # Fight Loop
    round = 0
    while team1.pets and team2.pets:
        pet1 = team1.pets[0]
        pet2 = team2.pets[0]

        round += 1

        log.debug(get_battle_string(team1, team2, prefix=f'Before Attack :'))

        pet1.before_attack()
        pet2.before_attack()

        log.debug(get_battle_string(team1, team2, prefix=f'Round ({round}):'))

        pet1.attack_pet(pet2)

        log.debug(get_battle_string(team1, team2, prefix=f'After Fight :'))

        if verbose:
            print(get_battle_string(team1, team2, prefix=f'After Fight :'))

        if not team1.pets:
            log.debug("Team 1 loses")
        if not team2.pets:
            log.debug("Team 2 loses")
        if not team1.pets and not team2.pets:
            log.debug("It's a tie!")
    # End of Battle
    log.debug("End of Battle")
    log.debug(get_battle_string(team1, team2, prefix=f'Final Board State :'))
    log.debug("Finished Fight")

    return [int(bool(team1.pets)), int(bool(team2.pets))]
