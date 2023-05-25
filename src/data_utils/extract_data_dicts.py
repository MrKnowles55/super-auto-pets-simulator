import json
import requests
from bs4 import BeautifulSoup


def load_old_data():
    url = "https://superauto.pet/api.json"
    response = requests.get(url)
    return json.loads(response.text)


def extract_unique_parameters(data):
    triggers = set()
    trigger_bys = set()
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
                trigger_by = ability.get("triggeredBy").get("kind")
                if trigger_by:
                    trigger_bys.add(trigger_by)

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
        'trigger_bys': list(trigger_bys),
        'effect_kinds': list(effect_kinds),
        'effect_target_kinds': list(effect_target_kinds)
    }


def load_pet_soup(pet):
    pet = pet.title().replace(" ","_")
    url = "https://superautopets.fandom.com/wiki/" + pet
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_ability_data(soup):
    level_data = soup.select(".pi-item.pi-data.pi-item-spacing.pi-border-color")

    abilities = {}
    for level in level_data:
        level_label = level.find("h3", class_="pi-data-label pi-secondary-font").text
        ability_description = level.find("div", class_="pi-data-value pi-font").text
        abilities[level_label] = ability_description.strip()
    # print(ability)
    return abilities


def get_tier_and_pack(soup, pet_name):
    pet_name = pet_name.title()

    # Find the correct paragraph starting with "The <b>Pet</b> is a..."
    paragraph = None
    for p in soup.find_all("p"):
        # Remove leading line breaks and spaces before checking the paragraph content
        paragraph_text = p.text.lstrip("\n ").rstrip("\n ")
        if paragraph_text.startswith(f"The {pet_name} is a"):
            paragraph = p
            break
    # Find the tier
    if paragraph:
        tier_a = paragraph.find("a", title=lambda x: x and "Tier" in x)
        if tier_a:
            tier = tier_a["title"]
        else:
            tier = "0"
    else:
        tier = "0"


    # Find the packs
    packs = []
    if paragraph:
        for tag in paragraph.find_all("b"):
            # print(f"tag{tag}")
            if "pack" in tag.text.lower() or "packs" in tag.text.lower():
                packs.append(tag.text.capitalize().split(" ")[0])
    output = {"tier": tier, "packs": packs}
    # print(output)
    return output


def load_new_pet(pet_name):
    pet_name = pet_name.title()
    soup = load_pet_soup(pet_name)
    abilities = get_ability_data(soup)
    tier_and_packs = get_tier_and_pack(soup, pet_name)
    output = {}
    output["name"] = pet_name
    output["id"] = "pet_utils-" + pet_name.replace(" ", "_").lower()
    output["tier"] = int(tier_and_packs["tier"].replace("Tier ", ""))
    if "Stats" in list(abilities.keys()):
        output["baseAttack"] = int(abilities["Stats"].split("/")[0])
        output["baseHealth"] = int(abilities["Stats"].split("/")[1])
    else:
        output["baseAttack"] = -1
        output["baseHealth"] = -1
    output["packs"] = tier_and_packs["packs"]
    try:
        output["level1Ability"] = {"description": abilities["Level 1"]}
        output["level2Ability"] = {"description": abilities["Level 2"]}
        output["level3Ability"] = {"description": abilities["Level 3"]}
    except KeyError:
        bad_output = {"name": output["name"], "id": output["id"]}
        return bad_output
    return output


if __name__ == "__main__":
    # Load the first JSON file as a dictionary
    with open(r'C:\Users\mrkno\PycharmProjects\super-auto-pets-simulator\data\pet_data.json') as f:
        dict1 = json.load(f)

    unique = extract_unique_parameters(dict1)
    for key, value in unique.items():
        print(key, value)
    #
    # # Load the second JSON file as a dictionary
    # with open('pet_data_mine.json') as f:
    #     dict2 = json.load(f)
    #
    # # Combine the two dictionaries
    # combined_dict = {**dict1, **dict2}
    #
    # # Print the combined dictionary
    # with open("pet_data.json", 'w') as file:
    #     json.dump(combined_dict, file, indent=4)
    # old_data = load_old_data()
    # PET_DICT = old_data["pets"]
    # FOOD_DICT = old_data["foods"]
    # STATUS_DICT = old_data["statuses"]
    # TURN_DICT = old_data["turns"]
    #
    # soup = load_pet_soup("bulldog")
    # get_ability_data(soup)
    # get_tier_and_pack(soup, "Bulldog")
    # print(load_new_pet("iguana"))
    # output = {}
    # with open("notes/pets_to_add", 'r') as file:
    #     lines = file.readlines()
    #     for line in lines:
    #         datum = line.lstrip("\n ").rstrip("\n ")
    #         if datum:
    #             if "Tier" in datum:
    #                 continue
    #             elif datum in ["Tiger", "Star", "Golden"]:
    #                 continue
    #             else:
    #                 new_pet = load_new_pet(datum)
    #                 output[new_pet["id"]] = new_pet
    # with open("pet_data_mine.json", 'w') as file:
    #     file.write(json.dumps(output, indent=4))

    # html = '<div class="pi-data-value pi-font"><b><a href="/wiki/Hurt_(Trigger)" title="Hurt (Trigger)">Hurt</a></b>: Set attack equal to health +1.</div>'
    #
    # soup = BeautifulSoup(html, 'html.parser')
    # div_element = soup.find('div', {'class': 'pi-data-value pi-font'})
    # text = div_element.text.strip()
    #
    # print(text)  # output: "Hurt: Set attack equal to health +1."


#
#     with open("pet_data_backup.json", 'w') as file:
#         file.write(json.dumps(PET_DICT, indent=4))

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
    #     for pet_utils in PET_DICT.values():
    #         ability = [pet_utils.get('level1Ability', {}),
    #                      pet_utils.get('level2Ability', {}),
    #                      pet_utils.get('level3Ability', {})]
    #
    #         for ability in ability:
    #             trigger = ability.get('trigger')
    #             if trigger == t:
    #                 if pet_utils["name"] not in trigger_list[t]:
    #                     trigger_list[t].append(pet_utils["name"])
    #     print(t, trigger_list[t])
    # effect_kinds_list = {}
    # for e in sorted(parameters["effect_kinds"]):
    #     effect_kinds_list[e] = []
    #     for pet_utils in PET_DICT.values():
    #         ability = [pet_utils.get('level1Ability', {}),
    #                      pet_utils.get('level2Ability', {}),
    #                      pet_utils.get('level3Ability', {})]
    #
    #         for ability in ability:
    #             effect = ability.get('effect')
    #             if effect:
    #                 effect_kind = effect.get('kind')
    #                 if effect_kind == e:
    #                     if pet_utils["name"] not in effect_kinds_list[e]:
    #                         effect_kinds_list[e].append(pet_utils["name"])
    #     print(e, effect_kinds_list[e])
    # effect_target_kinds_list = {}
    # for e in sorted(parameters["effect_target_kinds"]):
    #     effect_target_kinds_list[e] = []
    #     for pet_utils in PET_DICT.values():
    #         ability = [pet_utils.get('level1Ability', {}),
    #                      pet_utils.get('level2Ability', {}),
    #                      pet_utils.get('level3Ability', {})]
    #
    #         for ability in ability:
    #             effect = ability.get('effect')
    #             if effect:
    #                 target = effect.get('target')
    #                 if target:
    #                     target_kind = target.get('kind')
    #                     if target_kind == e:
    #                         if pet_utils["name"] not in effect_target_kinds_list[e]:
    #                             effect_target_kinds_list[e].append(pet_utils["name"])
    #     print(e, effect_target_kinds_list[e])



    # lst = []
    # d = {}

    # for pet_utils in list(PET_DICT.keys()):
    #     for v in PET_DICT[pet_utils].keys():
    #         for ability in ["level1Ability", "level2Ability", "level3Ability"]:
    #             foo = PET_DICT[pet_utils].get(ability)
    #             if not foo:
    #                 continue
    #             for key in foo.keys():
    #                 if isinstance(foo[key], dict):
    #                     d[key] = []
    #                     for kkey in foo[key].keys():
    #                         if kkey not in d[key]:
    #                             d[key].append(kkey)
    # print(d)