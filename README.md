# Protobufs Compiler

This project is a protobufs compiler that compiles Protocol Buffers (protobuf) definitions into either C source files or Python modules. The compilation is executed within a Docker container, ensuring a consistent and isolated build environment.

## Features

- **Multi-language Support**: Compile protobuf files to C or Python based on user input.
- **Docker Integration**: The compilation process is contained within a Docker container, simplifying dependencies and environment setup.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) installed on your machine.
- Basic knowledge of Protocol Buffers and the languages you want to compile to.

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/LucasDFranchi/TitaniumProto.git
   cd TitaniumProto
   ```

2. Build the Docker image:

   ```bash
   docker build -t protobuf-compiler .
   ```

### Usage

To compile a protobuf file, use the following command:

```bash
sh run.sh -fp input_file.proto -e output_type
```

Replace `<input_file.proto>` with the path to your protobuf file and `<output_type>` with either `c` for C files or `python` for Python modules.

### Example

To compile a protobuf file to Python, run:

```bash
sh run.sh -fp titanium.proto -e py
```

This will generate a Python module in the current directory.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
