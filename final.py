import argparse
import json
import os
import sys
import yaml

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The input file containing JSON or YAML data")
    parser.add_argument("output_file", help="The output file to save the JSON data")
    return parser.parse_args()

def loading_json(input_file):
    if not os.path.exists(input_file):
        print(f"No such file: {input_file}")
        sys.exit(1)
    
    with open(input_file, "r") as file_js:
        try:
            json_obj = json.load(file_js)
            return json_obj
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            sys.exit(1)

def loading_yaml(input_file):
    if not os.path.exists(input_file):
        print(f"No such file: {input_file}")
        sys.exit(1)
    
    with open(input_file, "r") as file_ym:
        try:
            yaml_obj = yaml.safe_load(file_ym)
            return yaml_obj
        except yaml.YAMLError as e:
            print(f"Error decoding YAML: {e}")
            sys.exit(1)

def save_json(obj, output_file):
    with open(output_file, "w") as file_js:
        json.dump(obj, file_js, indent=4)
    
def main():
    args = parse_arguments()
    input_file = args.input_file
    output_file = args.output_file

    file_extension = os.path.splitext(input_file)[1].lower()
    
    if file_extension == ".json":
        obj = loading_json(input_file)
    elif file_extension == ".yml" or file_extension == ".yaml":
        obj = loading_yaml(input_file)
    else:
        print("Input file is neither JSON nor YAML file")
        sys.exit(1)

    save_json(obj, output_file)

if __name__ == "__main__":
    main()


