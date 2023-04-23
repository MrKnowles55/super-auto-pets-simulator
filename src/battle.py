from utils import prioritize_pets, collect_triggered_abilities
from pet_data_utils.enums.trigger_event import TriggerEvent
from pet_data_utils.enums.effect_kind import EffectKind
from pet_data_utils.enums.effect_target_kind import EffectTargetKind
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


def start_of_battle(team1, team2, pet_list, verbose=False):
    actions = []
    priority_dict = prioritize_pets(pet_list)
    priorities = sorted(priority_dict.keys(), reverse=True)

    # Initialize applied damage dictionary
    applied_damage = {}

    for priority in priorities:
        pets_with_same_priority = priority_dict[priority]

        # Collect abilities that should trigger for StartOfBattle event
        triggered_abilities = []
        for pet in pets_with_same_priority:
            if pet.team == team1:
                triggered_abilities += collect_triggered_abilities([pet], TriggerEvent.StartOfBattle, priority,
                                                                   enemy_team=team2, applied_damage=applied_damage)
            else:
                triggered_abilities += collect_triggered_abilities([pet], TriggerEvent.StartOfBattle, priority,
                                                                   enemy_team=team1, applied_damage=applied_damage)

        # Execute the collected abilities
        for ability_priority, ability, enemy_team, applied_damage in triggered_abilities:
            actions += ability.apply(ability.owner, ability.owner.team, enemy_team=enemy_team, applied_damage=applied_damage)

        for action in actions:
            action_name, *args = action
            if action_name == "take_damage":
                pet, damage, attacker = args
                pet.apply_damage(damage, attacker)
    if verbose:
        print(get_battle_string(team1, team2, prefix="Start of Battle"))


def fight_loop(team1, team2, verbose=False):
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


def end_of_battle(team1, team2, verbose=False):
    # End of Battle
    log.debug("End of Battle")
    log.debug(get_battle_string(team1, team2, prefix=f'Final Board State :'))
    log.debug("Finished Fight")

    return [int(bool(team1.pets)), int(bool(team2.pets))]


def fight(team1, team2, verbose=False):
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
        print(get_battle_string(team1, team2, prefix='Before Fight :'))

    # Start of Battle
    pet_list = get_pet_list(team1, team2)

    priority_dict = prioritize_pets(pet_list)

    start_of_battle(team1, team2, pet_list, verbose)
    fight_loop(team1, team2, verbose)

    return end_of_battle(team1, team2, verbose)





