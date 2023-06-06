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

    @property
    def pets_list(self):
        return self.player_team.pets_list + self.enemy_team.pets_list

    # Main Loop
    def battle_loop(self):
        combat_turns = 0
        self.start_of_battle()
        while self.fighters[0] and self.fighters[1]:
            combat_turns += 1
            # print(f"Round {combat_turns}: {self.fighters}")
            self.fight_loop()
        return self.get_battle_result()

    # Utilities

    def get_battle_result(self):
        # 0 for tie, no changes made
        # +1 for win, score goes +1
        # -1 for loss, lives go -1
        return 0 if len(self.player_team) == len(self.enemy_team) == 0 else 1 if len(self.player_team) > 0 else -1

    # Actions and Signals

    def create_action(self, pet, ability_dict, trigger):
        if not ability_dict and not trigger:
            print("Placeholder text for Team.remove_pet()")
        ability_trigger = ability_dict.get("trigger")
        if ability_trigger == trigger:
            effect = ability_dict.get("effect")
            if effect:
                method = effect.get("kind")
            else:
                return
            effect_args = ability_dict.get("effect", {}).copy()
            effect_args.pop("kind", None)
            return Action(pet, method, **effect_args)
        return

    def enqueue(self, priority, action):
        self.action_queue.add_action(priority, action)

    def collect_actions(self, trigger_event, scope):
        for pet in scope:
            action = self.create_action(pet, pet.ability, trigger_event)
            if action:
                self.enqueue(pet.attack, action)

    # TriggerEvents
    def start_of_battle(self):
        self.collect_actions(TriggerEvent.StartOfBattle, self.pets_list)
        self.action_queue.execute_all()

    def before_attack(self):
        self.collect_actions(TriggerEvent.BeforeAttack, list(self.fighters))
        self.action_queue.execute_all()

    def after_attack(self, fighters):
        self.collect_actions(TriggerEvent.AfterAttack, list(fighters))
        self.action_queue.execute_all()

    # Combat
    def fight_loop(self):
        self._before_fight_events()
        self._fight_events()
        self._after_fight_events()

    def _before_fight_events(self):
        self.before_attack()

    def _fight_events(self):
        self._attack()

    def _after_fight_events(self):
        fighters = list(self.fighters)
        self.fighters[0].update()
        self.fighters[1].update()
        fighters = [pet for pet in fighters if pet.alive]
        self.after_attack(fighters)

    def _attack(self):
        self.fighters[0].attack_pet(self.fighters[1])
        self.fighters[1].attack_pet(self.fighters[0])






