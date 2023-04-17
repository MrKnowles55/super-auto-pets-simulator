# Super Auto Pets Simulator 

The Super Auto Pets Simulator is a Python program that simulates thousands of fights between different teams of pets in the Super Auto Pets game. By reverse engineering the game logic the simulator provides insights into how different pets and teams compare in terms of their performance in battles.

### Installation

To install and run the Super Auto Pets Simulator, follow these steps:

Clone the repository to your local machine: ```git clone https://github.com/MrKnowles55/super-auto-pets-simulator.git```
    
Install the required Python packages: ```pip install -r requirements.txt```
    
Run the simulator: ```python main.py```
Edit the config file to change simulation parameters: ```python config.py```

### Usage

To use the Super Auto Pets Simulator, you can customize the simulation settings by modifying the config.py file. You can specify the number of simulations to run, the teams to compare, and the pets to use in each team. After running the simulation, the program will output the results to the console (eventually it will return a file as well).

### How it Works

The Super Auto Pets Simulator works by simulating fights between different teams of pets. The program takes into account the pets' base stats, abilities, and synergies, as well as the opponent's team and any random effects that may occur during the fight.

The simulator runs multiple simulations to obtain a statistically significant sample size, and then uses the results to calculate the win rates and other performance metrics for each team. These metrics can be used to compare different pets and teams, and to gain insights into the underlying game mechanics of Super Auto Pets.

### Current State

- All pets included with base stats from all packs (as of January 11, 2023) with rough outline of abilities stored in data/pet_data.json (template from https://github.com/bencoveney/super-auto-pets-db)
- Some pet abilities implemented (Ant, Cricket, Betta Fish and Flamingo)

### Upcoming Features

- Complete ability system to generate abilities from pet_data.json
- Shop simulation: Buying and selling of pets, ordering, leveling_up, etc.
- Food and perks
- Statistical analysis of simulations, pets, and synergies
- In-Game overlay to capture your team and enemy team to provide into your real games!


### Contributing

If you would like to contribute to the Super Auto Pets Simulator, you can do so by submitting a pull request with your changes. Before submitting a pull request, please make sure to follow the project's coding standards and to write unit tests for your code.

### License

The Super Auto Pets Simulator is licensed under the MIT License.
