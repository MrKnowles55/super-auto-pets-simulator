import json
from jsonschema import validate, ValidationError
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
config_path = os.path.join(parent_dir, "config.json")
config_schema_path = os.path.join(parent_dir, "config_schema.json")


def load_config(config_file, schema_file):
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    with open(schema_file, 'r') as f:
        schema_data = json.load(f)

    try:
        validate(config_data, schema_data)
    except ValidationError as e:
        print(f"Error: {e.message}")
        sys.exit(1)

    return config_data


if __name__ == "__main__":
    config = load_config(config_path, config_schema_path)
    print("Config file is valid.")