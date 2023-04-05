import json
import requests

url = "https://superauto.pet/api.json"
response = requests.get(url)
data = json.loads(response.text)


PET_DICT = data["pets"]
FOOD_DICT = data["food"]
STATUS_DICT = data["statuses"]
TURN_DICT = data["turns"]