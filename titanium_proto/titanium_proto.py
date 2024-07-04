import argparse

from .src import TitaniumFileGenerator

def handle_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="This script runs inventory and collects data from Titanium protobuf files."
    )

    parser.add_argument(
        "--file_path", "-fp", 
        help="Specify the path to a single Titanium Protobuf file to process.",
        required=False
    )
    parser.add_argument(
        "--search_path", "-sp", 
        help="Specify a directory path to search and compile all Titanium Protobuf files found within it.",
        required=False
    )
    
    args = parser.parse_args()
    
    if not (args.file_path or args.search_path):
        parser.error("Need to specify either --file_path or --search_path.")

    return parser.parse_args()

def main():
    args = handle_arguments()
    tp = TitaniumFileGenerator()
    
    tp.import_and_parse_proto_file(args.file_path)
    tp.generate_cpp_file()


if __name__ == "__main__":
    main()
    