import argparse
import json
import os
import sys
import yaml
import xml.etree.ElementTree as ET

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The input file containing JSON, YAML, or XML data")
    parser.add_argument("output_file", help="The output file to save the data in JSON or YAML format")
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

def loading_xml(input_file):
    if not os.path.exists(input_file):
        print(f"No such file: {input_file}")
        sys.exit(1)
    
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
        xml_dict = ET_to_dict(root)
        return xml_dict
    except ET.ParseError as e:
        print(f"Error decoding XML: {e}")
        sys.exit(1)

def ET_to_dict(node):
    node_dict = {}
    if node.text:
        node_dict[node.tag] = node.text.strip()
    else:
        node_dict[node.tag] = {}

    for child in node:
        child_dict = ET_to_dict(child)
        if child.tag in node_dict[node.tag]:
            if not isinstance(node_dict[node.tag][child.tag], list):
                node_dict[node.tag][child.tag] = [node_dict[node.tag][child.tag]]
            node_dict[node.tag][child.tag].append(child_dict[child.tag])
        else:
            node_dict[node.tag].update(child_dict)
    
    return node_dict

def save_json(obj, output_file):
    with open(output_file, "w") as file_js:
        json.dump(obj, file_js, indent=4)

def save_yaml(obj, output_file):
    with open(output_file, "w") as file_ym:
        yaml.dump(obj, file_ym, default_flow_style=False)

def main():
    args = parse_arguments()
    input_file = args.input_file
    output_file = args.output_file

    input_extension = os.path.splitext(input_file)[1].lower()
    output_extension = os.path.splitext(output_file)[1].lower()
    
    if input_extension == ".json":
        obj = loading_json(input_file)
    elif input_extension == ".yml" or input_extension == ".yaml":
        obj = loading_yaml(input_file)
    elif input_extension == ".xml":
        obj = loading_xml(input_file)
    else:
        print("Input file is neither JSON, YAML, nor XML file")
        sys.exit(1)

    if output_extension == ".json":
        save_json(obj, output_file)
    elif output_extension == ".yml" or output_extension == ".yaml":
        save_yaml(obj, output_file)
    else:
        print("Output file extension is not supported (use .json or .yml/.yaml)")
        sys.exit(1)

if __name__ == "__main__":
    main()



