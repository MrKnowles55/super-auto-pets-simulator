# def filter_pets_by_ability_trigger(pet_list, trigger):
#     """
#     Filter a list of pets based on a given ability trigger.
#
#     :param pet_list: A list of pets to filter.
#     :param trigger: The trigger to filter pets by.
#     :return: A list of pets with the specified ability trigger.
#     """
#     return [pet for pet in pet_list if pet.ability.trigger_event == trigger]
#
#
# def sort_pets_by_attribute(pet_list, attribute, reverse=True):
#     """
#     Sort a list of pets based on a given attribute.
#
#     :param pet_list: A list of pets to sort.
#     :param attribute: The attribute to sort pets by.
#     :param reverse: Whether to sort the pets in descending order.
#     :return: A sorted list of pets based on the specified attribute.
#     """
#     return sorted(pet_list, key=lambda pet: getattr(pet, attribute), reverse=reverse)
#
#
# def get_lowest_health_pets(pet_list, n, reverse=False):
#     return sort_pets_by_attribute(pet_list, "health", reverse)[:n]
