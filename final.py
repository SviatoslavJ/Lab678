import argparse
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    return parser.parse_args()
def main():
    args = parse_arguments()
    input_file = args.input_file
    output_file = args.output_file
    if os.path.splitext(input_file)[1] == ".json":
        obj = loading_json(input_file)
def loading_json(input_file):
    for file in files:
        if file == input_file:
            with open(file, "r") as file_js:
                file_content = file_js.read()
                json_obj = json.loads(file_content)
                return json_obj
    print("No such file")
    sys.exit(1)
if name == "main":
    main()
