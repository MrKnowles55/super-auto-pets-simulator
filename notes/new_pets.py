import json


class NewPet:
    def __init__(self, name, tier, base_attack, base_health, packs, ability_description, ability_trigger,
                 ability_triggered_by, ability_effect_kind, **ability_effect_kwargs):
        self.name = name
        self.id = 'pet_utils-' + self.name.lower().replace(" ", "-")
        self.image = {
            "source": "",
            "commit": "",
            "unicodeCodePoint": ""
        }
        self.tier = tier
        self.baseAttack = base_attack
        self.baseHealth = base_health
        self.packs = packs

        ability_template = {
            "description": "",
            "trigger": "",
            "triggeredBy": "",  # WRONG
            "effect": {}
        }
        self.level1Ability = None
        self.level2Ability = None
        self.level3Ability = None
        abilities = {"1": self.level1Ability, "2": self.level2Ability, "3": self.level3Ability}
        for level in ["1", "2", "3"]:
            description = ability_description[level]
            trigger = ability_trigger[level]
            triggeredby = {"kind": ability_triggered_by[level]}
            effect = {"kind": ability_effect_kind[level]}
            for key, value in ability_effect_kwargs.items():
                effect[key] = value[level]

            parameters = [description, trigger, triggeredby, effect]
            abilities[level] = {k: v for k, v in zip(ability_template.keys(), parameters)}
        self.level1Ability = abilities["1"]
        self.level2Ability = abilities["2"]
        self.level3Ability = abilities["3"]

        self.probabilities = []


new_pet = NewPet(name="Ant", tier=1, base_attack=2, base_health=1, packs=["StandardPack", "ExpansionPack1"],
                 ability_description={"1": "Faint: Give a random friend +2/+1",
                                      "2": "Faint: Give a random friend +4/+2",
                                      "3": "Faint: Give a random friend +6/+3"},
                 ability_trigger={"1": "Faint",
                                  "2": "Faint",
                                  "3": "Faint"
                                  },
                 ability_triggered_by={"1": "Self",
                                       "2": "Self",
                                       "3": "Self"},
                 ability_effect_kind={"1": "ModifyStats",
                                      "2": "ModifyStats",
                                      "3": "ModifyStats"},
                 attackAmount={"1": 2,
                               "2": 4,
                               "3": 6},
                 healthAmount={"1": 1,
                               "2": 2,
                               "3": 3},
                 target={"1": {"kind": "RandomFriend", "n": 1},
                         "2": {"kind": "RandomFriend", "n": 1},
                         "3": {"kind": "RandomFriend", "n": 1}},
                 untilEndOfBattle={"1": False,
                                   "2": False,
                                   "3": False}
                 )
print(json.dumps(new_pet.__dict__, indent=4))

if input("Save???").lower() in ["yes", "y", 1, "1"]:
    with open("pet_data_mine.json", 'w') as file:
        file.write(json.dumps(new_pet.__dict__, indent=4))
