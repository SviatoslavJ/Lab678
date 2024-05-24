import json
import os
import sys
import yaml
import xml.etree.ElementTree as ET
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, OptionMenu, messagebox

def loading_json(input_file):
    with open(input_file, "r") as file_js:
        try:
            json_obj = json.load(file_js)
            return json_obj
        except json.JSONDecodeError as e:
            raise Exception(f"Error decoding JSON: {e}")

def loading_yaml(input_file):
    with open(input_file, "r") as file_ym:
        try:
            yaml_obj = yaml.safe_load(file_ym)
            return yaml_obj
        except yaml.YAMLError as e:
            raise Exception(f"Error decoding YAML: {e}")

def loading_xml(input_file):
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
        xml_dict = ET_to_dict(root)
        return xml_dict
    except ET.ParseError as e:
        raise Exception(f"Error decoding XML: {e}")

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

def convert_files(input_file, output_file):
    input_extension = os.path.splitext(input_file)[1].lower()
    output_extension = os.path.splitext(output_file)[1].lower()
    
    if input_extension == ".json":
        obj = loading_json(input_file)
    elif input_extension in [".yml", ".yaml"]:
        obj = loading_yaml(input_file)
    elif input_extension == ".xml":
        obj = loading_xml(input_file)
    else:
        raise Exception("Input file is neither JSON, YAML, nor XML file")

    if output_extension == ".json":
        save_json(obj, output_file)
    elif output_extension in [".yml", ".yaml"]:
        save_yaml(obj, output_file)
    elif output_extension == ".xml":
        save_xml(obj, output_file)
    else:
        raise Exception("Output file extension is not supported (use .json, .yml/.yaml, or .xml)")

def browse_input():
    filename = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("JSON files", "*.json"), ("YAML files", "*.yml *.yaml"), ("XML files", "*.xml")])
    input_path.set(filename)

def browse_output():
    filename = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json"), ("YAML files", "*.yml *.yaml"), ("XML files", "*.xml")])
    output_path.set(filename)

def run_conversion():
    input_file = input_path.get()
    output_file = output_path.get()
    if not input_file or not output_file:
        messagebox.showerror("Error", "Both input and output files must be selected")
        return

    try:
        convert_files(input_file, output_file)
        messagebox.showinfo("Success", f"File converted and saved to {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = Tk()
app.title("File Converter")

input_path = StringVar()
output_path = StringVar()

Label(app, text="Input File:").grid(row=0, column=0, padx=10, pady=10)
Entry(app, textvariable=input_path, width=50).grid(row=0, column=1, padx=10, pady=10)
Button(app, text="Browse", command=browse_input).grid(row=0, column=2, padx=10, pady=10)

Label(app, text="Output File:").grid(row=1, column=0, padx=10, pady=10)
Entry(app, textvariable=output_path, width=50).grid(row=1, column=1, padx=10, pady=10)
Button(app, text="Browse", command=browse_output).grid(row=1, column=2, padx=10, pady=10)

Button(app, text="Convert", command=run_conversion).grid(row=2, column=0, columnspan=3, pady=20)

app.mainloop()





