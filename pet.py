class Pet:
    def __init__(self, name, attack, health, ability):
        self.name = name
        self.attack = attack
        self.health = health
        self.ability = ability
        self.team = None
        self.fainted = False

    def __str__(self):
        return f"{self.name}({self.attack}/{self.health})"

    def is_alive(self):
        return self.health > 0

    def attack_pet(self, enemy_pet):
        self.health -= enemy_pet.attack
        enemy_pet.health -= self.attack

        # if not self.is_alive() or not enemy_pet.is_alive():
        #     if not self.is_alive():
        #         self.ability.trigger("faint", self, self.team, enemy_team=enemy_pet.team)
        #         self.team.remove_pet(self)
        #     if not enemy_pet.is_alive():
        #         enemy_pet.ability.trigger("faint", enemy_pet, enemy_pet.team, enemy_team=self.team)
        #         enemy_pet.team.remove_pet(enemy_pet)
        #
        #     # Clean up dead pets after abilities have been triggered
        #     if not self.is_alive():
        #         self.team.remove_pet(self)
        #     if not enemy_pet.is_alive():
        #         enemy_pet.team.remove_pet(enemy_pet)

        if not self.is_alive() or not enemy_pet.is_alive():
            if not self.is_alive():
                self.ability.trigger("faint", self, self.team, enemy_team=enemy_pet.team)
            if not enemy_pet.is_alive():
                enemy_pet.ability.trigger("faint", enemy_pet, enemy_pet.team, enemy_team=self.team)

            # Clean up dead pets after abilities have been triggered
            if not self.is_alive() and self in self.team.pets:
                self.team.remove_pet(self)
            if not enemy_pet.is_alive() and enemy_pet in enemy_pet.team.pets:
                enemy_pet.team.remove_pet(enemy_pet)

    def faint(self):
        if not self.fainted:
            self.fainted = True
            if self.ability:
                self.ability.trigger("faint", self, self.team)

    def apply_ability(self, team, enemy_team):
        self.ability.apply(self, team, enemy_team)

    def start_of_battle(self, enemy_team):
        if self.ability:
            self.ability.trigger("start_of_battle", self, self.team, enemy_team=enemy_team)

    def damaged(self):
        if self.ability:
            self.ability.trigger("damaged", self, self.team)

        if not self.is_alive() and not self.fainted:
            self.faint()
            self.team.remove_pet(self)

    def before_attack(self):
        if self.ability:
            self.ability.trigger("before_attack", self, self.team)


def prioritize_pets(pet_list, priority_key=lambda x: x.attack):
    sorted_pets = sorted(pet_list, key=priority_key, reverse=True)

    priority_dict = {}
    for pet in sorted_pets:
        priority = priority_key(pet)
        if priority not in priority_dict:
            priority_dict[priority] = []
        priority_dict[priority].append(pet)

    return priority_dict




