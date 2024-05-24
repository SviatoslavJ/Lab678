import argparse
import json
import os
import sys

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The input file containing JSON data")
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

def save_json(obj, output_file):
    with open(output_file, "w") as file_js:
        json.dump(obj, file_js, indent=4)
    
def main():
    args = parse_arguments()
    input_file = args.input_file
    output_file = args.output_file
    
    if os.path.splitext(input_file)[1] == ".json":
        obj = loading_json(input_file)
        save_json(obj, output_file)
    else:
        print("Input file is not a JSON file")
        sys.exit(1)

if __name__ == "__main__":
    main()

