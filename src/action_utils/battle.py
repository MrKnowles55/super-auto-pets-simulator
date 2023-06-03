from src.action_utils.action import PriorityQueue, Action

from src.data_utils.enums.trigger_event import TriggerEvent
from src.data_utils.enums.trigger_by_kind import TriggerByKind
from src.data_utils.enums.effect_target_kind import EffectTargetKind
from src.data_utils.enums.effect_kind import EffectKind


class Battle:
    def __init__(self, player_team, enemy_team):
        self.player_team = player_team
        self.enemy_team = enemy_team
        self.action_queue = PriorityQueue()

        self.player_team.action_handler = self
        self.enemy_team.action_handler = self

    @property
    def fighters(self):
        return self.player_team.first, self.enemy_team.first

    # Utilities

    def get_pet_list(self):
        return self.player_team.pets_list + self.enemy_team.pets_list

    # Actions and Signals

    def create_action(self, pet, ability_dict, trigger):
        if not ability_dict and not trigger:
            print("Placeholder text for Team.remove_pet()")
        ability_trigger = ability_dict.get("trigger")
        if ability_trigger == trigger:
            method = ability_dict.get("effect")
            effect_args = ability_dict.get("effect_dict")
            return Action(pet, method, **effect_args)
        return None

    def enqueue(self, priority, action):
        self.action_queue.add_action(priority, action)

    # TriggerEvents
    def start_of_battle(self):
        for pet in self.get_pet_list():
            action = self.create_action(pet, pet.ability, TriggerEvent.StartOfBattle)
            if action:
                self.enqueue(pet.attack, action)

    def before_attack(self):
        pass

    def after_attack(self):
        pass

    # Phases
    def before_combat(self):
        pass

    def during_combat(self):
        self.combat()

    def combat(self):
        self.fighters[0].attack_pet(self.fighters[1])
        self.fighters[1].attack_pet(self.fighters[0])
        # print(f"Before: {pre_fight_info} | After: {(fighters[0].combat_stats, fighters[1].combat_stats)}")

    def after_combat(self):
        self.fighters[0].update()
        self.fighters[1].update()

    def fight_loop(self):
        self.before_combat()
        self.during_combat()
        self.after_combat()

    def battle_loop(self):
        combat_turns = 0
        print(f"{list(reversed(self.player_team.pets_list))} VS {self.enemy_team.pets_list}")
        while self.fighters[0] and self.fighters[1]:
            combat_turns += 1
            print(f"Round {combat_turns}: {self.fighters}")
            self.fight_loop()
        print(f"{list(reversed(self.player_team.pets_list))} VS {self.enemy_team.pets_list}")




