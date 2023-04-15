def prioritize_pets(pets, key_func, reverse=False):
    return sorted(pets, key=key_func, reverse=reverse)