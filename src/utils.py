def prioritize_pets(pet_list, priority_key=lambda x: x.attack):
    """
    Create a dictionary of pets prioritized by a given attribute.

    :param pet_list: A list of pets to prioritize.
    :param priority_key: A function that takes a pet and returns a value to prioritize the pet by.
    :return: A dictionary where keys are priorities and values are lists of pets with that priority.
    """
    sorted_pets = sorted(pet_list, key=priority_key, reverse=True)

    priority_dict = {}
    for pet in sorted_pets:
        priority = priority_key(pet)
        if priority not in priority_dict:
            priority_dict[priority] = []
        priority_dict[priority].append(pet)

    return priority_dict


def filter_pets_by_ability_trigger(pet_list, trigger):
    """
    Filter a list of pets based on a given ability trigger.

    :param pet_list: A list of pets to filter.
    :param trigger: The trigger to filter pets by.
    :return: A list of pets with the specified ability trigger.
    """
    return [pet for pet in pet_list if pet.ability.trigger_event == trigger]


def sort_pets_by_attribute(pet_list, attribute, reverse=True):
    """
    Sort a list of pets based on a given attribute.

    :param pet_list: A list of pets to sort.
    :param attribute: The attribute to sort pets by.
    :param reverse: Whether to sort the pets in descending order.
    :return: A sorted list of pets based on the specified attribute.
    """
    return sorted(pet_list, key=lambda pet: getattr(pet, attribute), reverse=reverse)


def get_lowest_health_pets(pet_list, n, reverse=False):
    return sort_pets_by_attribute(pet_list, "health", reverse)[:n]


def collect_triggered_abilities(pet_list, trigger_event, priority, enemy_team=None, applied_damage=None):
    triggered_abilities = []
    for pet in pet_list:
        if pet.ability and pet.ability.trigger_event == trigger_event:
            triggered_abilities.append((priority, pet.ability, enemy_team, applied_damage))
    return triggered_abilities


