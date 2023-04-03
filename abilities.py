from abc import ABC, abstractmethod
from random import choice
from pet import prioritize_pets


class Ability(ABC):
    @abstractmethod
    def apply(self, pet, team,  **kwargs):
        pass

    @abstractmethod
    def trigger(self, event, *args, **kwargs):
        pass

    def __repr__(self):
        attributes = ', '.join([f"{k}={repr(v)}" for k, v in vars(self).items()])
        return f"{self.__class__.__name__}({attributes})"


class No_Ability(Ability):
    def __init__(self):
        pass

    def apply(self, pet, team,  **kwargs):
        pass

    def trigger(self, event, *args, **kwargs):
        pass


class Summon(Ability):
    def __init__(self, token, trigger_event):
        self.token = token
        self.trigger_event = trigger_event

    def apply(self, pet, team,  **kwargs):
        from pet_factory import create_pet
        if self.trigger_event == "faint":

            index = team.pets.index(pet)

            try:
                new_pet = create_pet(self.token)
                team.remove_pet(pet)
                team.add_pet(new_pet, index)
            except KeyError:
                print(f"Cannot create pet of type {self.token}")
                team.remove_pet(pet)

        else:
            print(f'{self.__class__}:{self.trigger_event} not implemented')

    def trigger(self, event, *args, **kwargs):
        if event == self.trigger_event:
            self.apply(*args, **kwargs)


class Damage(Ability):
    def __init__(self, damage, target, trigger_event):
        self.damage = damage
        self.target = target
        self.trigger_event = trigger_event

    def apply(self, pet, team, **kwargs):
        enemy_team = kwargs.get('enemy_team', None)
        if enemy_team is None:
            pass
            # print(f'Error: enemy_team is not provided for {self}')
            # raise ValueError
        if self.target == "random_enemy":
            if enemy_team.pets:
                alive_pets = [p for p in enemy_team.pets if p.is_alive()]

                if alive_pets:
                    target_pet = choice(alive_pets)
                else:
                    target_pet = None
                if target_pet:
                    target_pet.health -= self.damage
                    target_pet.hurt()
        elif self.target == "all":
            targets = []
            # Damage the pets
            if team:
                for pet in team.pets:
                    if pet.is_alive():
                        pet.health -= self.damage
                        targets.append(pet)
            if enemy_team:
                for pet in enemy_team.pets:
                    if pet.is_alive():
                        pet.health -= self.damage
                        targets.append(pet)
            priority_dict = prioritize_pets(targets)
            for target in sorted(priority_dict.keys(), reverse=True):
                pets_with_same_priority = priority_dict[target]
                for pet in pets_with_same_priority:
                    pet.hurt()
        elif self.target == "friend_behind":
            index = team.pets.index(pet)
            if index < 5 and len(team.pets) > 1:
                target = team.pets[index+1]

                if target:
                    target.health -= self.damage
                    target.hurt()
        else:
            print(f'{self.__class__}:{self.target} not implemented')

    def trigger(self, event, *args, **kwargs):
        if event == self.trigger_event:
            self.apply(*args, **kwargs)


class ModifyStatsAbility(Ability):
    def __init__(self, attack_change, health_change, target, trigger_event, buff_length=0):
        self.attack_change = attack_change
        self.health_change = health_change
        self.target = target
        self.trigger_event = trigger_event

    def apply(self, pet, team,  **kwargs):
        if self.target == "random_friendly":
            # Create a list of friendly pets, excluding the triggering pet
            available_targets = [p for p in team.pets if p is not pet and p.health > 0]

            # Check if there are available targets
            if available_targets:
                # Choose a random pet from the available targets
                target_pet = choice(available_targets)

                # Modify the target pet's stats
                target_pet.attack += self.attack_change
                target_pet.health += self.health_change
        elif self.target == "front_most_friend":
            if team.pets:
                target = team.pets[0]
                target.attack += self.attack_change
        elif self.target == "self":
            pet.attack += self.attack_change
            pet.health += self.health_change
        elif self.target == "2_friends_behind":
            index = team.pets.index(pet)
            pet_count = len(team.pets)
            if pet_count > 1:
                if index == pet_count - 2:
                    behind_1 = team.pets[index+1]
                    behind_1.attack += self.attack_change
                    behind_1.health += self.health_change
                elif pet_count - index >= 3:
                    behind_1 = team.pets[index+1]
                    behind_1.attack += self.attack_change
                    behind_1.health += self.health_change
                    behind_2 = team.pets[index+2]
                    behind_2.attack += self.attack_change
                    behind_2.health += self.health_change
        else:
            print(f'{self.__class__}:{self.target} not implemented')

    def trigger(self, event, *args, **kwargs):
        if event == self.trigger_event:
            self.apply(*args, **kwargs)
