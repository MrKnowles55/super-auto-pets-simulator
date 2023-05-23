from src.config_utils.logger import setup_logger, log_call, log_class_init
from src.action.action_utils import action_handler, generate_remove_action
from src.actions import PriorityQueue, Action
import signals

log = setup_logger(__name__)


class Team:
    def __init__(self, name):
        self.name = name
        self.pets_list = []
        self.action_handler = None

    def __str__(self):
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
            print("Remove Pet Not implemented without action handler")

    def move_pet(self, old_index, new_index):
        if 0 <= old_index < len(self.pets_list) and 0 <= new_index < len(self.pets_list):
            pet = self.pets_list.pop(old_index)
            self.pets_list.insert(new_index, pet)
            self.update_positions()
        else:
            try:
                pet = self.pets_list[old_index]
                log.debug(f"{self} cannot move {pet} from {old_index} to {new_index}")
            except IndexError:
                log.debug(f"{self} has no pet at {old_index} to move.")

    def fill(self):
        self.pets_list = [pet for pet in self.pets_list if pet is not None]
        self.update_positions()

    def update_positions(self):
        for pet in self.pets_list:
            pet.update_position(self.pets_list.index(pet))

    def create_action(self, pet, ability_dict, trigger):
        ability_trigger = ability_dict.get("trigger")
        if ability_trigger == trigger:
            method = ability_dict.get("effect")
            effect_args = ability_dict.get("effect_dict")
            return Action(pet, method, **effect_args)
        return None

    def send_action(self, action):
        if action:
            if self.action_handler:
                self.action_handler.action_queue.add_action(action.pet.attack, action)

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


