import argparse
import json
import os
import sys
import yaml
import xml.etree.ElementTree as ET

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The input file containing JSON, YAML, or XML data")
    parser.add_argument("output_file", help="The output file to save the data in JSON, YAML, or XML format")
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
    node_dict = {node.tag: {} if node.attrib else None}
    children = list(node)
    if children:
        dd = {}
        for dc in map(ET_to_dict, children):
            for k, v in dc.items():
                if k in dd:
                    if not isinstance(dd[k], list):
                        dd[k] = [dd[k]]
                    dd[k].append(v)
                else:
                    dd[k] = v
        node_dict = {node.tag: dd}
    if node.attrib:
        node_dict[node.tag].update(('@' + k, v) for k, v in node.attrib.items())
    if node.text:
        text = node.text.strip()
        if children or node.attrib:
            if text:
                node_dict[node.tag]['#text'] = text
        else:
            node_dict[node.tag] = text
    return node_dict

def dict_to_ET(d):
    def _to_etree(d, root):
        if not d:
            pass
        elif isinstance(d, str):
            root.text = d
        elif isinstance(d, list):
            for item in d:
                elem = ET.Element(root.tag)
                root.append(elem)
                _to_etree(item, elem)
        elif isinstance(d, dict):
            for k, v in d.items():
                if k.startswith('@'):
                    root.set(k[1:], v)
                elif k == '#text':
                    root.text = v
                else:
                    elem = ET.Element(k)
                    root.append(elem)
                    _to_etree(v, elem)
        else:
            root.text = str(d)
        return root

    assert isinstance(d, dict) and len(d) == 1
    tag, body = next(iter(d.items()))
    node = ET.Element(tag)
    return ET.ElementTree(_to_etree(body, node))

def save_json(obj, output_file):
    with open(output_file, "w") as file_js:
        json.dump(obj, file_js, indent=4)

def save_yaml(obj, output_file):
    with open(output_file, "w") as file_ym:
        yaml.dump(obj, file_ym, default_flow_style=False)

def save_xml(obj, output_file):
    tree = dict_to_ET(obj)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

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
    elif output_extension == ".xml":
        save_xml(obj, output_file)
    else:
        print("Output file extension is not supported (use .json, .yml/.yaml, or .xml)")
        sys.exit(1)

if __name__ == "__main__":
    main()




