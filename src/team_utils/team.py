from src.config_utils.logger import setup_logger
from src.action_utils.action import Action
from src.action_utils import signals

log = setup_logger(__name__)


class Team:
    def __init__(self, name):
        self.name = name
        self.pets_list = []
        self.action_handler = None

    def __str__(self):
        return self.name + " Team"

    def __repr__(self):
        return self.name + " Team"

    @property
    def length(self):
        return len(self.pets_list)

    @property
    def first(self):
        if self.length:
            return self.pets_list[0]
        else:
            return None

    def add_pet(self, pet, index=None):
        if len(self.pets_list) < 5:
            if index is not None:
                self.pets_list.insert(index, pet)
            else:
                self.pets_list.append(pet)
            pet.team = self
            self.update_positions()
        else:
            log.debug(f"{self} is full and cannot add {pet} at index {index}.")

    def remove_pet(self, pet):
        if self.action_handler:
            self.action_handler.create_action(pet, None, None)
        else:
            print("Remove Pet Not implemented without action_utils handler")

    def move_pet(self, old_index, new_index):
        if 0 <= old_index < len(self.pets_list):
            if 0 <= new_index < 5:
                pet = self.pets_list.pop(old_index)
                self.pets_list.insert(new_index, pet)
                self.update_positions()

    # def fill(self):
    #     self.pets_list = [pet for pet in self.pets_list if pet is not None]
    #     self.update_positions()

    def update_positions(self):
        for pet in self.pets_list:
            pet.update_position(self.pets_list.index(pet))

    def create_action(self, pet, ability_dict, trigger):
        ability_trigger = ability_dict.get("trigger")
        if ability_trigger == trigger:
            method = ability_dict.get("effect").get("kind")
            effect_args = {}
            for key,value in ability_dict.get("effect").items():
                if key != "kind":
                    effect_args[key] = value
            return Action(pet, method, **effect_args)
        return None

    def send_action(self, action):
        if action:
            if self.action_handler:
                self.action_handler.enqueue(action.pet.attack, action)

    def send_signal(self, message, receiver, sender=None, broadcast=False):
        if sender:
            signals.send_signal(message, sender, receiver, broadcast)
        else:
            signals.send_signal(message, self, receiver, broadcast)

    def read_signal(self, signal, broadcast):
        message = signal.message
        sender = signal.sender
        for pet in self.pets_list:
            receiver = pet
            self.send_signal(message, receiver, sender)
        if broadcast:
            other_team = self.action_handler.player_team if self != self.action_handler.player_team else self.action_handler.enemy_team
            self.send_signal(message, other_team,sender, broadcast=False)


