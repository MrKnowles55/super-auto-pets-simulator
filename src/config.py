import os
import json

parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
config_path = os.path.join(parent_dir, "config.json")

# Simulation Parameters
SIMULATIONS_TO_RUN = 5000

# Friendly Team Parameters
FRIENDLY_TEAM_SIZE = 5  # 1 through 5

# Enemy Team Parameters
ENEMY_TEAM_SIZE = 5  # 1 through 5

# Other
DEBUG_MODE = True


def save_data(data, filename=config_path):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_data(filename=config_path):
    with open(filename, "r") as file:
        return json.load(file)


def display(data):
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    config_data = load_data()
    display(config_data)
