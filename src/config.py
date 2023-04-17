import os
import json

parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
config_path = os.path.join(parent_dir, "config.json")
schema_path = os.path.join(parent_dir, "config_schema.json")


class ConfigHandler:
    def __init__(self, config_file=config_path, schema_file=schema_path):
        self.config_file = config_file
        self.schema_file = schema_file
        self.config_data = self.load_data()
        self.schema_data = self.load_data(filename=schema_file)

    def save_data(self, filename=None):
        if filename is None:
            filename = self.config_file
        with open(filename, "w") as file:
            json.dump(self.config_data, file, indent=4)

    def load_data(self, filename=None):
        if filename is None:
            filename = self.config_file
        with open(filename, "r") as file:
            return json.load(file)

    def display(self):
        print(json.dumps(self.config_data, indent=4))

    def display_allowed_values(self, parameter_name):
        try:
            print("Allowed values: ", self.schema_data["properties"][parameter_name]["enum"])
        except KeyError:
            try:
                property_type = self.schema_data["properties"][parameter_name]["type"]
                if property_type == "integer":
                    minimum = self.schema_data["properties"][parameter_name].get("minimum", "None")
                    maximum = self.schema_data["properties"][parameter_name].get("maximum", "None")
                    print(f"Allowed values: {property_type} with minimum {minimum} and maximum {maximum}.")
            except KeyError:
                print(f"Parameter {parameter_name} not found in schema")

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

            # Convert the input to the appropriate type
            new_value = self.convert_input(new_value, parameter_value_type)

            if new_value is None:
                print(f"{parameter_name} must be type: {parameter_value_type.__name__}")
                return

            # Validate the new value
            if not self.is_value_valid(parameter_name, new_value):
                return

            if new_value == self.config_data[parameter_name]:
                print(f"Parameter {parameter_name} is already set to {new_value}")
            else:
                self.config_data[parameter_name] = new_value
                self.save_data()
        else:
            print(f"Parameter {parameter_name} not found.")

    def convert_input(self, input_value, target_type):
        try:
            if target_type == int:
                return int(input_value)
            elif target_type == float:
                return float(input_value)
            elif target_type == bool:
                return input_value.lower() == "true"
            else:
                return input_value
        except ValueError:
            return None

    def is_value_valid(self, parameter_name, new_value):
        min_value = self.schema_data["properties"][parameter_name].get("minimum", None)
        max_value = self.schema_data["properties"][parameter_name].get("maximum", None)

        if min_value is not None and new_value < min_value:
            print(f"{parameter_name} must be greater than or equal to {min_value}")
            return False

        if max_value is not None and new_value > max_value:
            print(f"{parameter_name} must be less than or equal to {max_value}")
            return False

        if parameter_name in ["FRIENDLY_TEAM_POOL", "ENEMY_TEAM_POOL"] and not self.is_enum_valid(parameter_name, new_value):
            print(
                f"{parameter_name} must be one of the following: {', '.join(self.schema_data['properties'][parameter_name]['enum'])}")
            return False

        return True

    def is_enum_valid(self, parameter_name, value):
        enum_values = self.schema_data["properties"][parameter_name].get("enum", None)
        if enum_values is None:
            return True
        return value in enum_values


config_handler = ConfigHandler()


def main():
    run = True
    while run:
        print("\n")
        config_handler.display()
        parameter_to_change = input("What parameter would you like to change? ").upper()
        if parameter_to_change and parameter_to_change.lower() not in ["no", "none"]:
            config_handler.display_allowed_values(parameter_to_change)
            new_parameter_value = input("Enter new value: ")
            config_handler.set_parameter(parameter_to_change, new_parameter_value)
        else:
            run = input("Are you done changing parameters? ")
            if run and run.lower() in ["y", "yes", "1"]:
                run = False


if __name__ == "__main__":
    main()

