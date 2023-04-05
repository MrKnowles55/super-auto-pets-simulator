import json
import requests

url = "https://superauto.pet/api.json"
response = requests.get(url)
data = json.loads(response.text)


PET_DICT = data["pets"]
FOOD_DICT = data["foods"]
STATUS_DICT = data["statuses"]
TURN_DICT = data["turns"]

if __name__ == "__main__":
    # Pretty-print the data
    # new_dict = {key: {sub_key: sub_value for sub_key, sub_value in value.items() if sub_key != 'probabilities'} for
    #             key, value in PET_DICT.items()}

    pretty_data = json.dumps(PET_DICT, indent=2)
    print(pretty_data)