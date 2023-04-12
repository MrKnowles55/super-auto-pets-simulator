from .ability import *
from .modify_stats import *


class AbilityGenerator:

    def __init__(self, ability_dict, owner):
        self.ability_dict = ability_dict
        self.owner = owner

    def get_trigger(self):
        return self.ability_dict.get("trigger")

    def get_triggered_by(self):
        return self.ability_dict.get("triggeredBy", {}).get("kind")

    def get_attack_mod(self):
        return self.ability_dict.get("effect", {}).get("attackAmount")

    def get_health_mod(self):
        return self.ability_dict.get("effect", {}).get("healthAmount")

    def get_target(self):
        return self.ability_dict.get("effect", {}).get("target")

    def get_target_n(self):
        return self.ability_dict.get("effect", {}).get("target", {}).get("n")

    def get_target_kind(self):
        return self.ability_dict.get("effect", {}).get("target", {}).get("kind")

    def get_extra(self):
        keys_to_exclude = ["description", "trigger", "triggeredBy", "effect"]
        return {key: value for key, value in self.ability_dict.items() if key not in keys_to_exclude}

    def get_extra_effect(self):
        keys_to_exclude = ["kind", "attackAmount", "healthAmount", "target"]
        effects = self.ability_dict.get("effect")
        if effects:
            return {key: value for key, value in effects.items() if key not in keys_to_exclude}
        else:
            return {}

    def get_ability_type(self):
        if self.ability_dict:
            return self.ability_dict.get("effect").get("kind")
        else:
            return None

    def generate(self):
        ability_type = self.get_ability_type()
        match ability_type:
            case "ModifyStats":
                return self.generate_modify_stats_ability()
            case _:
                return No_Ability(self.owner)

    def generate_modify_stats_ability(self):
        attack_mod = self.get_attack_mod()
        health_mod = self.get_health_mod()
        target_type = self.get_target_kind()
        target_n = self.get_target_n()
        trigger = self.get_trigger()

        match target_type:
            case "RandomFriend":
                return ModifyStatsAbilityRandomFriend(self.owner, attack_mod=attack_mod, health_mod=health_mod,
                                                      target_type=target_type, target_n=target_n, trigger_event=trigger)
            case _:
                return No_Ability(self.owner)
