from random import choice
from team.team import Team
from pet_factory import create_pet
from pet_data_utils import pet_data_manager
from battle import fight
from config import config_handler
import validate_config
from logger import setup_logger


def create_random_team(pet_pool, team_size=5):
    team = Team()
    for _ in range(team_size):
        random_pet = choice(list(pet_pool))
        team.add_pet(create_pet(random_pet))
    return team


def run_simulation(num_sims, friendly_pool, enemy_pool, friendly_team_size=5, enemy_team_size=5):
    total = [0, 0]

    for i in range(num_sims):
        friendly_team = create_random_team(friendly_pool, team_size=friendly_team_size)
        enemy_team = create_random_team(enemy_pool, team_size=enemy_team_size)
        result = fight(friendly_team, enemy_team)
        total[0] += result[0]
        total[1] += result[1]

    return total, num_sims


def main(sims, friendly_team_size=5, enemy_team_size=5, friendly_pool=pet_data_manager.TEST_POOL,
         enemy_pool=pet_data_manager.TEST_POOL2):

    total, num_sims = run_simulation(sims, friendly_pool, enemy_pool, friendly_team_size, enemy_team_size)

    win_rate = total[0] / num_sims
    loss_rate = total[1] / num_sims
    tie_rate = (num_sims - total[0] - total[1]) / num_sims

    print("Battle Results")
    print(f'Rounds: {num_sims}, Wins {win_rate:.1%}, Losses {loss_rate:.1%}, Ties {tie_rate:.1%}')


if __name__ == "__main__":

    # Configure Logging
    logger = setup_logger(__name__)
    logger.debug("Logging in DEBUG mode.")

    # Validate config.json matches config_schema.json
    validate_config.load_config()

    # Load config data
    NUMBER_OF_SIMULATIONS = config_handler.config_data['NUMBER_OF_SIMULATIONS']
    FRIENDLY_TEAM_SIZE = config_handler.config_data['FRIENDLY_TEAM_SIZE']
    ENEMY_TEAM_SIZE = config_handler.config_data['ENEMY_TEAM_SIZE']
    FRIENDLY_POOL_ID = config_handler.config_data['FRIENDLY_TEAM_POOL']
    ENEMY_POOL_ID = config_handler.config_data['ENEMY_TEAM_POOL']
    FRIENDLY_TEAM_POOL = pet_data_manager.pet_db.pool_dict[FRIENDLY_POOL_ID]
    ENEMY_TEAM_POOL = pet_data_manager.pet_db.pool_dict[ENEMY_POOL_ID]

    print(f"--------------------------------"
          f"\nRunning {NUMBER_OF_SIMULATIONS} simulations with Parameters:\n\n"
          f"\tFriendly Team Size: {FRIENDLY_TEAM_SIZE}\n"
          f"\tEnemy Team Size: {ENEMY_TEAM_SIZE}\n"
          f"\tFriendly Team Pool: {FRIENDLY_POOL_ID}\n"
          f"\tEnemy Team Pool: {ENEMY_POOL_ID}\n"
          f"--------------------------------"
          )

    main(sims=NUMBER_OF_SIMULATIONS,
         friendly_team_size=FRIENDLY_TEAM_SIZE,
         enemy_team_size=ENEMY_TEAM_SIZE,
         friendly_pool=FRIENDLY_TEAM_POOL,
         enemy_pool=ENEMY_TEAM_POOL)
