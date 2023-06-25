import random


class Targeter:
    def __init__(self):
        pass
    # Friends
    def target_adjacent_friends(self, caller, **kwargs):
        possible_targets = caller.team.pets_list
        n = min(kwargs.get("n", 1), len(possible_targets) - 1)
        origin = possible_targets.index(caller)

        start = max(0, origin - n)  # Ensure start is not less than 0
        end = min(len(possible_targets), origin + n + 1)  # Ensure end is not more than length of list
        targets = possible_targets[start:origin] + possible_targets[origin + 1:end]
        return targets

    def target_different_tier_animals(self, caller, **kwargs):
        # Should be friends not animals
        possible_targets = [pet for pet in caller.team.pets_list if pet != caller]
        pets_by_tier = {i: [] for i in range(1, 7)}
        for pet in possible_targets:
            pets_by_tier[pet.tier].append(pet)

        # Sample one pet from each tier
        targets = [random.choice(pets_by_tier[tier]) for tier in pets_by_tier if pets_by_tier[tier]]

        return targets

    def target_each_friend(self, caller, **kwargs):
        return [pet for pet in caller.team.pets_list if pet != caller]

    def target_friend_ahead(self, caller, **kwargs):
        n = kwargs.get("n", 1)
        index = caller.team.pets_list.index(caller)  # Get index of caller in list
        start = max(0, index - n)  # Make sure the start index isn't negative
        return caller.team.pets_list[start:index][::-1]  # Slice and reverse the list

    def target_friend_behind(self, caller, **kwargs):
        n = kwargs.get("n", 1)
        index = caller.team.pets_list.index(caller)  # Get index of caller in list
        end = min(len(caller.team.pets_list),
                  index + n + 1)  # Make sure the end index doesn't exceed the length of the list
        return caller.team.pets_list[index + 1:end]  # Slice the list

    def target_level2_and_3_friends(self, caller, **kwargs):
        possible_targets = [pet for pet in caller.team.pets_list if pet != caller and pet.level != 1]
        n = min(kwargs.get("n", 1), len(possible_targets))
        return random.sample(possible_targets, n)

    def target_random_friend(self, caller, **kwargs):
        possible_targets = [pet for pet in caller.team.pets_list if pet != caller]
        n = min(kwargs.get("n", 1), len(possible_targets))
        targets = random.sample(possible_targets, n)
        return targets

    def target_right_most_friend(self, caller, **kwargs):
        return [caller.team.pets_list[0]]

    # Enemies
    def target_each_enemy(self, caller, **kwargs):
        return caller.team.other_team.pets_list

    def target_first_enemy(self, caller, **kwargs):
        return [caller.team.other_team.pets_list[0]]

    def target_highest_health_enemy(self, caller, **kwargs):
        return [sorted(caller.team.other_team.pets_list, key=lambda x: x.health, reverse=True)[0]]

    def target_lowest_health_enemy(self, caller, **kwargs):
        return [sorted(caller.team.other_team.pets_list, key=lambda x: x.health, reverse=False)[0]]

    def target_last_enemy(self, caller, **kwargs):
        return [caller.team.other_team.pets_list[-1]]

    def target_random_enemy(self, caller, **kwargs):
        possible_targets = caller.team.other_team.pets_list
        n = min(kwargs.get("n", 1), len(possible_targets))
        targets = random.sample(possible_targets, n)
        return targets

    # Shop

    # @staticmethod
    # def target_each_shop_animal(**kwargs):
    #     return kwargs
    #
    # @staticmethod
    # def target_left_most_shop_animal(**kwargs):
    #     return kwargs

    # Other
    def target_self(self, caller, **kwargs):
        return [caller]

    def target_all(self, caller, **kwargs):
        # only used for faint abilities, may need to remove caller from targets
        return caller.team.pets_list + caller.team.other_team.pets_list

    def target_adjacent_animals(self, caller, **kwargs):
        possible_targets = caller.team.pets_list[::-1] + caller.team.other_team.pets_list
        n = min(kwargs.get("n", 1), len(possible_targets) - 1)
        origin = possible_targets.index(caller)

        start = max(0, origin - n)  # Ensure start is not less than 0
        end = min(len(possible_targets), origin + n + 1)  # Ensure end is not more than length of list
        targets = possible_targets[start:origin] + possible_targets[origin + 1:end]

        return targets

    @staticmethod
    def target_triggering_entity(**kwargs):
        return [kwargs.get("triggering_entity", None)]

    @staticmethod
    def target_test_target(**kwargs):
        return [kwargs]


class Targeter_Multi:
    def __init__(self, pet):
        self.pet = pet

    # Friends
    def target_adjacent_friends(self, **kwargs):
        possible_targets = self.pet.team.pets_list
        n = min(kwargs.get("n", 1), len(possible_targets) - 1)
        origin = possible_targets.index(self.pet)

        start = max(0, origin - n)  # Ensure start is not less than 0
        end = min(len(possible_targets), origin + n + 1)  # Ensure end is not more than length of list
        targets = possible_targets[start:origin] + possible_targets[origin + 1:end]
        return targets

    def target_different_tier_animals(self, **kwargs):
        # Should be friends not animals
        possible_targets = [pet for pet in self.pet.team.pets_list if pet != self.pet]
        pets_by_tier = {i: [] for i in range(1, 7)}
        for pet in possible_targets:
            pets_by_tier[pet.tier].append(pet)

        # Sample one pet from each tier
        targets = [random.choice(pets_by_tier[tier]) for tier in pets_by_tier if pets_by_tier[tier]]

        return targets

    def target_each_friend(self, **kwargs):
        return [pet for pet in self.pet.team.pets_list if pet != self.pet]

    def target_friend_ahead(self, **kwargs):
        n = kwargs.get("n", 1)
        index = self.pet.team.pets_list.index(self.pet)  # Get index of self in list
        start = max(0, index - n)  # Make sure the start index isn't negative
        return self.pet.team.pets_list[start:index][::-1]  # Slice and reverse the list

    def target_friend_behind(self, **kwargs):
        n = kwargs.get("n", 1)
        index = self.pet.team.pets_list.index(self.pet)  # Get index of self in list
        end = min(len(self.pet.team.pets_list),
                  index + n + 1)  # Make sure the end index doesn't exceed the length of the list
        return self.pet.team.pets_list[index + 1:end]  # Slice the list

    def target_level2_and_3_friends(self, **kwargs):
        possible_targets = [pet for pet in self.pet.team.pets_list if pet != self.pet and pet.level != 1]
        n = min(kwargs.get("n", 1), len(possible_targets))
        return random.sample(possible_targets, n)

    def target_random_friend(self, **kwargs):
        possible_targets = [pet for pet in self.pet.team.pets_list if pet != self.pet]
        n = min(kwargs.get("n", 1), len(possible_targets))
        targets = random.sample(possible_targets, n)
        return targets

    def target_right_most_friend(self, **kwargs):
        return [self.pet.team.pets_list[0]]

    # Enemies
    def target_each_enemy(self, **kwargs):
        return self.pet.team.other_team.pets_list

    def target_first_enemy(self, **kwargs):
        return [self.pet.team.other_team.pets_list[0]]

    def target_highest_health_enemy(self, **kwargs):
        return [sorted(self.pet.team.other_team.pets_list, key=lambda x: x.health, reverse=True)[0]]

    def target_lowest_health_enemy(self, **kwargs):
        return [sorted(self.pet.team.other_team.pets_list, key=lambda x: x.health, reverse=False)[0]]

    def target_last_enemy(self, **kwargs):
        return [self.pet.team.other_team.pets_list[-1]]

    def target_random_enemy(self, **kwargs):
        possible_targets = self.pet.team.other_team.pets_list
        n = min(kwargs.get("n", 1), len(possible_targets))
        targets = random.sample(possible_targets, n)
        return targets

    # Shop

    # @staticmethod
    # def target_each_shop_animal(**kwargs):
    #     return kwargs
    #
    # @staticmethod
    # def target_left_most_shop_animal(**kwargs):
    #     return kwargs

    # Other
    def target_self(self, **kwargs):
        return [self.pet]

    def target_all(self, **kwargs):
        # only used for faint abilities, may need to remove self from targets
        return self.pet.team.pets_list + self.pet.team.other_team.pets_list

    def target_adjacent_animals(self, **kwargs):
        possible_targets = self.pet.team.pets_list[::-1] + self.pet.team.other_team.pets_list
        n = min(kwargs.get("n", 1), len(possible_targets) - 1)
        origin = possible_targets.index(self.pet)

        start = max(0, origin - n)  # Ensure start is not less than 0
        end = min(len(possible_targets), origin + n + 1)  # Ensure end is not more than length of list
        targets = possible_targets[start:origin] + possible_targets[origin + 1:end]

        return targets

    @staticmethod
    def target_triggering_entity(**kwargs):
        return [kwargs.get("triggering_entity", None)]

    @staticmethod
    def target_test_target(**kwargs):
        return [kwargs]
