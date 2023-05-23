from actions import PriorityQueue, Action


class Battle:
    def __init__(self, player_team, enemy_team):
        self.player_team = player_team
        self.enemy_team = enemy_team
        self.action_queue = PriorityQueue()

        self.player_team.action_handler = self
        self.enemy_team.action_handler = self

    def get_pet_list(self):
        return self.player_team.pets_list + self.enemy_team.pets_list

    def start_of_battle(self):
        for pet in self.get_pet_list():
            action = self.create_action(pet, pet.ability, "Start of Battle")
            if action:
                self.action_queue.add_action(pet.attack, action)

    def create_action(self, pet, ability_dict, trigger):
        if not ability_dict and not trigger:
            print("Placeholder text for Team.remove_pet()")
        ability_trigger = ability_dict.get("trigger")
        if ability_trigger == trigger:
            method = ability_dict.get("effect")
            effect_args = ability_dict.get("effect_dict")
            return Action(pet, method, **effect_args)
        return None





