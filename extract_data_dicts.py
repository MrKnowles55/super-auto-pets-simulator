import json
import requests

url = "https://superauto.pet/api.json"
response = requests.get(url)
data = json.loads(response.text)


PET_DICT = data["pets"]
FOOD_DICT = data["foods"]
STATUS_DICT = data["statuses"]
TURN_DICT = data["turns"]


def extract_unique_parameters(data):
    triggers = set()
    effect_kinds = set()
    effect_target_kinds = set()

    for pet in data.values():
        abilities = [pet.get('level1Ability', {}),
                     pet.get('level2Ability', {}),
                     pet.get('level3Ability', {})]

        for ability in abilities:
            trigger = ability.get('trigger')
            if trigger:
                triggers.add(trigger)

            effect = ability.get('effect')
            if effect:
                effect_kind = effect.get('kind')
                if effect_kind:
                    effect_kinds.add(effect_kind)

                target = effect.get('target')
                if target:
                    target_kind = target.get('kind')
                    if target_kind:
                        effect_target_kinds.add(target_kind)

    return {
        'triggers': list(triggers),
        'effect_kinds': list(effect_kinds),
        'effect_target_kinds': list(effect_target_kinds)
    }


if __name__ == "__main__":

    with open("pet_data_backup.json", 'w') as file:
        file.write(json.dumps(PET_DICT, indent=4))

    # Pretty-print the data
    # new_dict = {key: {sub_key: sub_value for sub_key, sub_value in value.items() if sub_key not in
    #                   ['probabilities', 'image', 'notes']} for key, value in PET_DICT.items()}
    #
    # pretty_data = json.dumps(new_dict, indent=2)
    # print(pretty_data)
    # parameters = extract_unique_parameters(new_dict)
    #
    # print(parameters)
    #
    # trigger_list = {}
    # for t in sorted(parameters["triggers"]):
    #     trigger_list[t] = []
    #     for pet in PET_DICT.values():
    #         abilities = [pet.get('level1Ability', {}),
    #                      pet.get('level2Ability', {}),
    #                      pet.get('level3Ability', {})]
    #
    #         for ability in abilities:
    #             trigger = ability.get('trigger')
    #             if trigger == t:
    #                 if pet["name"] not in trigger_list[t]:
    #                     trigger_list[t].append(pet["name"])
    #     print(t, trigger_list[t])
    # effect_kinds_list = {}
    # for e in sorted(parameters["effect_kinds"]):
    #     effect_kinds_list[e] = []
    #     for pet in PET_DICT.values():
    #         abilities = [pet.get('level1Ability', {}),
    #                      pet.get('level2Ability', {}),
    #                      pet.get('level3Ability', {})]
    #
    #         for ability in abilities:
    #             effect = ability.get('effect')
    #             if effect:
    #                 effect_kind = effect.get('kind')
    #                 if effect_kind == e:
    #                     if pet["name"] not in effect_kinds_list[e]:
    #                         effect_kinds_list[e].append(pet["name"])
    #     print(e, effect_kinds_list[e])
    # effect_target_kinds_list = {}
    # for e in sorted(parameters["effect_target_kinds"]):
    #     effect_target_kinds_list[e] = []
    #     for pet in PET_DICT.values():
    #         abilities = [pet.get('level1Ability', {}),
    #                      pet.get('level2Ability', {}),
    #                      pet.get('level3Ability', {})]
    #
    #         for ability in abilities:
    #             effect = ability.get('effect')
    #             if effect:
    #                 target = effect.get('target')
    #                 if target:
    #                     target_kind = target.get('kind')
    #                     if target_kind == e:
    #                         if pet["name"] not in effect_target_kinds_list[e]:
    #                             effect_target_kinds_list[e].append(pet["name"])
    #     print(e, effect_target_kinds_list[e])



    # lst = []
    # d = {}

    # for pet in list(PET_DICT.keys()):
    #     for v in PET_DICT[pet].keys():
    #         for ability in ["level1Ability", "level2Ability", "level3Ability"]:
    #             foo = PET_DICT[pet].get(ability)
    #             if not foo:
    #                 continue
    #             for key in foo.keys():
    #                 if isinstance(foo[key], dict):
    #                     d[key] = []
    #                     for kkey in foo[key].keys():
    #                         if kkey not in d[key]:
    #                             d[key].append(kkey)
    # print(d)