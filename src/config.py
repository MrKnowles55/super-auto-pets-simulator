import os
import json

parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
config_path = os.path.join(parent_dir, "config.json")



class ConfigHandler:
    def __init__(self, filename=config_path):
        self.filename = filename
        self.config_data = self.load_data()

    def save_data(self,filename=None):
        if filename is None:
            filename = self.filename
        with open(filename, "w") as file:
            json.dump(self.config_data, file, indent=4)

    def load_data(self, filename=None):
        if filename is None:
            filename = self.filename
        with open(filename, "r") as file:
            return json.load(file)

    def display(self):
        print(json.dumps(self.config_data, indent=4))

    def set_sims_to_run(self, new_value):
        if isinstance(new_value, int) and new_value > 0:
            if "NUMBER_OF_SIMULATIONS" in self.config_data.keys():
                self.config_data["NUMBER_OF_SIMULATIONS"] = new_value
                self.save_data()
            else:
                print("NUMBER_OF_SIMULATIONS key not found")
        else:
            print("Enter a positive integer")

    def get_parameter(self, parameter_name):
        if parameter_name in self.config_data.keys():
            return self.config_data[parameter_name]

    def set_parameter(self, parameter_name, new_value):
        if parameter_name in self.config_data.keys():
            parameter_value_type = type(self.get_parameter(parameter_name))
            if parameter_value_type == type(new_value):
                if new_value == self.config_data[parameter_name]:
                    print(f"Parameter {parameter_name} is already set to {new_value}")
                    return
                else:
                    self.config_data[parameter_name] = new_value
                    self.save_data()
            else:
                print(f"{parameter_name} needs to be type: {parameter_value_type.__name__}")
        else:
            print(f"Parameter {parameter_name} not found.")


config_handler = ConfigHandler()


if __name__ == "__main__":
    config_handler = ConfigHandler()
    config_handler.display()
    config_handler.set_parameter("NUMBER_OF_SIMULATIONS", 55)
    config_handler.display()
