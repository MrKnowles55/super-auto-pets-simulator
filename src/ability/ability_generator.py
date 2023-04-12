from .ability import *
from .modify_stats import *
from src.pet_data_utils.enums.effect_kind import EffectKind
from src.pet_data_utils.enums.effect_target_kind import EffectTargetKind
from src.pet_data_utils.enums.trigger_event import TriggerEvent


class AbilityGenerator:

    def __init__(self, ability_dict, owner):
        self.ability_dict = ability_dict
        self.owner = owner

    def get_trigger(self):
        trigger_str = self.ability_dict.get("trigger")
        # Convert the string to the corresponding Trigger enum value
        return TriggerEvent[trigger_str]

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
        if self.ability_dict:
            effect_target_kind_str = self.ability_dict.get("effect", {}).get("target", {}).get("kind")
            # Convert the string to the corresponding EffectKind enum value
            return EffectTargetKind[effect_target_kind_str]
        else:
            return None

    def get_extra(self):
        keys_to_exclude = ["description", "trigger", "triggeredBy", "effect"]
        return {key: value for key, value in self.ability_dict.items() if key not in keys_to_exclude}

    def get_effect_pet(self):
        return self.ability_dict.get("effect", {}).get("pet")

    def get_effect_team(self):
        return self.ability_dict.get("effect", {}).get("team")

    def get_extra_effect(self):
        keys_to_exclude = ["kind", "attackAmount", "healthAmount", "target"]
        effects = self.ability_dict.get("effect")
        if effects:
            return {key: value for key, value in effects.items() if key not in keys_to_exclude}
        else:
            return {}

    def get_ability_type(self):
        if self.ability_dict:
            effect_kind_str = self.ability_dict.get("effect").get("kind")
            return EffectKind[effect_kind_str]  # Convert the string to the corresponding EffectKind enum value
        else:
            return None

    def generate(self):
        ability_type = self.get_ability_type()
        match ability_type:
            case EffectKind.ModifyStats:
                return self.generate_modify_stats_ability()
            case EffectKind.SummonPet:
                return self.generate_summon_ability()
            case _:
                return No_Ability(self.owner)

    def generate_summon_ability(self):
        trigger = self.get_trigger()
        pet_to_summon = self.get_effect_pet()
        team_to_summon_to = self.get_effect_team()

        match team_to_summon_to:
            case "Friendly":
                return Summon(self.owner, pet_to_summon, trigger, team_to_summon_to=team_to_summon_to)
            case _:
                return No_Ability(self.owner)

    def generate_modify_stats_ability(self):
        attack_mod = self.get_attack_mod()
        health_mod = self.get_health_mod()
        target_type = self.get_target_kind()
        target_n = self.get_target_n()
        trigger = self.get_trigger()

        match target_type:
            case EffectTargetKind.RandomFriend:
                return ModifyStatsAbilityRandomFriend(self.owner, attack_mod=attack_mod, health_mod=health_mod,
                                                      target_type=target_type, target_n=target_n, trigger_event=trigger)
            case _:
                return No_Ability(self.owner)
