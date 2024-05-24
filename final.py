def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    return parser.parse_args()
def main():
    args = parse_arguments()
    input_file = args.input_file
    output_file = args.output_file
if name == "main":
    main()
