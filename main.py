from random import choice
from team import Team
from pet_factory import create_pet
import pet_dict
from battle import fight

total = [0, 0]
sims = 5

friendly_pool = pet_dict.TEST_POOL
enemy_pool = pet_dict.TEST_POOL

for i in range(1, sims+1):
    friendly_team = Team()
    enemy_team = Team()

    for _ in range(5):
        friendly_team.add_pet(create_pet(choice(list(friendly_pool))))
        enemy_team.add_pet(create_pet(choice(list(enemy_pool))))
    verbose = bool(not(sims > 10))
    debug_friendly_team_list = friendly_team.pets[:]
    debug_enemy_team_list = enemy_team.pets[:]
    result = fight(friendly_team, enemy_team, verbose=verbose)
    total[0] += result[0]
    total[1] += result[1]
print(f'Rounds: {i}, Wins {total[0]/i:.1%}, Losses {total[1]/i:.1%}, Ties {(i-total[0]-total[1])/i:.1%}')
