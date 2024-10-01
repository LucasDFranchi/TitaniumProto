import argparse
import time
import os

def parse_arguments():
    """
    Parse command-line arguments.

    This function sets up the argument parser, defines the required arguments
    for the file path and file extension, and returns the parsed arguments.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Process file paths and extensions.')
    parser.add_argument('-fp', '--filepath', type=str, required=True, 
                        help='The file path to be processed.')
    parser.add_argument('-e', '--extension', type=str, required=True, 
                        choices=['py', 'c'], 
                        help='The file extension to process (either "py" for Python files or "c" for C files).')
    return parser.parse_args()

def get_filename_and_extension(filepath: str) -> str:
    """
    Extract the filename and extension from a given file path.

    Args:
        filepath (str): The full path to the file.

    Returns:
        str: The filename with its extension.
    """
    return os.path.basename(filepath)

def write_proto_file(filepath: str, content: str) -> None:
    """
    Write content to a file.

    This function attempts to open the specified file in write mode and 
    writes the provided content to it. If the file cannot be opened or 
    written to, it raises an IOError.

    Args:
        filepath (str): The path to the file where content will be written.
        content (str): The content to write to the file.

    Raises:
        IOError: If the file cannot be opened or written to.
    """
    try:
        with open(filepath, 'w') as file:
            file.write(content)
    except IOError as e:
        raise IOError(f"Error writing to file '{filepath}': {e}")


def read_proto_file(filepath: str = "/app/nanopb/generator/proto/nanopb.proto") -> str:
    """
    Read the contents of a Proto file.

    This function attempts to open and read the contents of the specified file.
    If the file cannot be found or opened, it raises an IOError.

    Args:
        filepath (str): The path to the file to read. Defaults to the 
                        nanopb.proto file.

    Returns:
        str: The contents of the file as a string.

    Raises:
        IOError: If the file cannot be opened or read.
    """
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error reading file '{filepath}': {e}")

def create_python_module(filepath: str):
    """
    Create a Python module directory based on the given file path.

    This function creates a directory named after the file (without extension)
    in the output folder and copies resource files into it.

    Args:
        filepath (str): The path to the Python file being processed.

    Returns:
        str: The name of the created module (directory) without the extension.
    """
    filename = os.path.basename(filepath)
    filename_without_extension = os.path.splitext(filename)[0]
    os.makedirs(f"/app/output/{filename_without_extension}", exist_ok=True)
    
    source_dir = "/app/resources/"
    destination_dir = f"/app/output/{filename_without_extension}/"
    os.system("ls -lah && cd resources && ls -lah")
    if os.path.exists(source_dir) and os.listdir(source_dir):
        os.system(f"cp {source_dir}* {destination_dir}")
    else:
        print(f"No files to copy from {source_dir} or directory does not exist.")

    return filename_without_extension

def process_python_file(filepath: str):
    """
    Process a Python file.

    This function reads the contents of the specified Python Proto file,
    modifies it, writes the modified content to a temporary file, and 
    generates a Python module based on the Proto definitions.

    Args:
        filepath (str): The path to the Python Proto file to process.

    Raises:
        IOError: If there are errors reading from or writing to files.
    """
    nanopb_file = read_proto_file()
    proto_file = read_proto_file(filepath).replace('syntax = "proto2";', '')
    
    temp_file = proto_file.replace('import "nanopb.proto";', nanopb_file)
    write_proto_file(os.path.join("/app/tmp/titanium_tmp.proto"), temp_file)

    module_name = create_python_module(filepath)
    os.system(f"cd /app/tmp/ && protoc --python_out=/app/output/{module_name} titanium_tmp.proto")

def process_c_file(filepath: str):
    """
    Process the C file.

    This function performs operations specific to C file processing. 
    Currently, it uses the nanopb generator to process a specified Proto file.

    Args:
        filepath (str): The path to the C Proto file to process.
    """
    os.system("cd /app/ && nanopb_generator -C -D /app/output titanium.proto")
    
def main():
    """
    Main function to execute the script.

    This function parses command-line arguments and directs processing
    to the appropriate function based on the specified file extension.
    """
    args = parse_arguments()
    
    if args.extension == 'py':
        process_python_file(args.filepath)
    elif args.extension == 'c':
        process_c_file(args.filepath)

if __name__ == "__main__":
    main()
