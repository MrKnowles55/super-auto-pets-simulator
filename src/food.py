import json


# class DataManager:
#     def __init__(self):
#         with open("../data/perk_data.json") as f:
#             self.data = json.load(f)


class Food:
    def __init__(self, name, **kwargs):
        self.name = name

        template = self._get_data()["foods"]["food-"+self.id]

        # Set to Template
        for key, value in template.items():
            if key != "id":
                setattr(self, key, value)

        # set additional attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def id(self):
        return self.name.lower().replace(" ", "-")

    def _get_data(self, source="../data/perk_data.json"):
        with open(source) as f:
            return json.load(f)


if __name__ == "__main__":
    foo = Food("Apple")
    for k,v in foo.__dict__.items():
        print(k, v)