from random import choice
from team.team import Team
from pet_factory import create_pet
from pet_data_utils import pet_data_manager
from battle import fight
import config

def create_random_team(pet_pool, team_size=5):
    team = Team()
    for _ in range(team_size):
        team.add_pet(create_pet(choice(list(pet_pool))))
    return team


def run_simulation(num_sims, friendly_pool, enemy_pool, verbose=False, friendly_team_size=5, enemy_team_size=5):
    total = [0, 0]

    for i in range(num_sims):
        friendly_team = create_random_team(friendly_pool, team_size=friendly_team_size)
        enemy_team = create_random_team(enemy_pool, team_size=enemy_team_size)
        result = fight(friendly_team, enemy_team, verbose=verbose)
        total[0] += result[0]
        total[1] += result[1]

    return total, num_sims


def main(sims, friendly_team_size=5, enemy_team_size=5, friendly_pool=pet_data_manager.TEST_POOL,
         enemy_pool=pet_data_manager.TEST_POOL2):
    verbose = sims <= 5

    total, num_sims = run_simulation(sims, friendly_pool, enemy_pool, verbose, friendly_team_size, enemy_team_size)

    win_rate = total[0] / num_sims
    loss_rate = total[1] / num_sims
    tie_rate = (num_sims - total[0] - total[1]) / num_sims

    print("Battle Results")
    print(f'Rounds: {num_sims}, Wins {win_rate:.1%}, Losses {loss_rate:.1%}, Ties {tie_rate:.1%}')


if __name__ == "__main__":
    print(f"\nRunning {config.SIMULATIONS_TO_RUN} simulations with Parameters:\n"
          f"Friendly Team Size: {config.FRIENDLY_TEAM_SIZE}\n"
          f"Enemy Team Size: {config.ENEMY_TEAM_SIZE}\n")
    main(sims=config.SIMULATIONS_TO_RUN,
         friendly_team_size=config.FRIENDLY_TEAM_SIZE,
         enemy_team_size=config.ENEMY_TEAM_SIZE)
